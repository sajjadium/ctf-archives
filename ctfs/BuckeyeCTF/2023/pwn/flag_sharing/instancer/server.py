import hashlib
import random
import string
import socket
from socketserver import ThreadingTCPServer, StreamRequestHandler
from multiprocessing import TimeoutError
from multiprocessing.pool import ThreadPool
import threading
import subprocess
import os, time
import base64
from pathlib import Path
import shutil
import requests
from proxyprotocol.v2 import ProxyProtocolV2
from proxyprotocol.reader import ProxyProtocolReader
from proxyprotocol import ProxyProtocolWantRead
from pow import get_challenge, verify_challenge, SOLVER_URL
import logging

logger = logging.getLogger(__name__)

PORT_BASE = int(os.getenv("CHAL_PORT_BASE", "7000"))
IP_BASE = "10.0.{}.3"
IFACE = "eth{}"
POW_DIFFICULTY = int(os.getenv("POW_DIFFICULTY", "0"))
NUM_SERVERS = int(os.getenv("CHAL_NUM_SERVERS", "5"))
DEBUG = int(os.getenv("DEBUG", "0")) == 1

# These are required attributes
CHAL_NET_PREFIX = os.environ["CHAL_NET_PREFIX"] # set by setup.sh
CHAL_IMAGE_NAME = os.environ["CHAL_IMAGE_NAME"] # set by docker-compose.yml

MY_IP = None

class MyTCPServer(ThreadingTCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 10)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 3)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)
        self.socket.bind(self.server_address)

pool = None

class MyTCPHandler(StreamRequestHandler):
    menu_state: int
    def setup(self):
        super().setup()
        self.menu_state = 0

    def handle(self):
        try:
            if not DEBUG:
                self.pp_result = read_proxy2(self)
                if not self.pp_result or not send_pow(self):
                    return
            else:
                if not send_pow(self):
                    return

            res = pool.apply_async(worker, (self,))
            pos = pool._inqueue.qsize()  # type: ignore
            self.wfile.write(f"[*] Queued in position {pos}\n".encode())
            res.get(timeout=180)

        except (ConnectionError, TimeoutError) as e:
            print("connection err: %s" % (e))
            pass

def read_proxy2(req: MyTCPHandler):
    pp_reader = ProxyProtocolReader(ProxyProtocolV2())
    pp_data = bytearray()
    while True:
        try:
            return pp_reader._parse(pp_data)
        except ProxyProtocolWantRead as want_read:
            try:
                if want_read.want_bytes is not None:
                    pp_data += req.rfile.read(want_read.want_bytes)
                elif want_read.want_line:
                    pp_data += req.rfile.readline()
                else:
                    print("ProxyProtocolWantRead of unknown length")
                    return None
            except (EOFError, ConnectionResetError) as exc:
                print("EOF waiting for proxy data")
                return None


def send_pow(req: MyTCPHandler):
    if POW_DIFFICULTY == 0:
        req.wfile.write(b"== proof-of-work: disabled ==\n")
        req.wfile.flush()
        return True

    challenge = get_challenge(POW_DIFFICULTY)

    req.wfile.write(b"== proof-of-work: enabled ==\n")
    req.wfile.write(b"please solve a pow first\n")
    req.wfile.write(b"You can run the solver with:\n")
    req.wfile.write("    python3 <(curl -sSL {}) solve {}\n".format(SOLVER_URL, challenge).encode())
    req.wfile.write(b"===================\n")
    req.wfile.write(b"\n")
    req.wfile.write(b"Solution? ")
    req.wfile.flush()
    solution = ''
    while not solution:
        solution = req.rfile.readline().decode("utf-8").strip()

    if verify_challenge(challenge, solution):
        req.wfile.write(b"Correct\n")
        req.wfile.flush()
        return True
    else:
        req.wfile.write(b"Proof-of-work fail")
        req.wfile.flush()
        return False

thread_to_port = {}
thread_port_lock = threading.Lock()

def get_port(ident):
    global thread_to_port
    thread_port_lock.acquire()

    if ident in thread_to_port:
        port = thread_to_port[ident]
    else:
        port = len(thread_to_port) + PORT_BASE + 2 # leave .0 and .1 unused
        thread_to_port[ident] = port

    thread_port_lock.release()
    return port

def is_socket_closed(sock) -> bool:
    try:
        # this will try to read bytes without blocking and also without removing them from buffer (peek only)
        data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
        if len(data) == 0:
            return True
        return False
    except BlockingIOError:
        return False  # socket is open and reading from it would block
    except ConnectionResetError:
        return True  # socket was closed for some other reason
    except OSError as e:
        if e.errno == 9: # Bad file descriptor
            return True
        else:
            logger.exception(f"unexpected exception when checking if a socket is closed: {e}")
    except Exception as e:
        logger.exception(f"unexpected exception when checking if a socket is closed: {e}")
    return False



def process_command(req: MyTCPHandler, bot_network_name):
    req.request.setblocking(False)

    bot_container_id = None
    try:
        # State 0: Main menu
        if req.menu_state == 0:
            line = req.rfile.readline()

            # Option 1: Spawn with real flag
            if line == b"1\n":
                req.menu_state = 3

                bot_spawn = subprocess.run(["./spawn_bot.sh", bot_network_name, ""], timeout=3, stdout=subprocess.PIPE, check=True, text=True)
                bot_container_id = bot_spawn.stdout.split("\n")[0]
                req.wfile.write(b"[+] Bot spawned using real flag\n")
            # Option 2: Spawn with fake flag
            elif line == b"2\n":
                req.menu_state = 1
                req.wfile.write(b"Enter your desired flag: ")

        # State 1: Waiting for fake flag
        elif req.menu_state == 1:
            line = req.rfile.readline()
            if len(line) > 1:
                line = line.decode('utf-8').split("\n")[0]
                req.menu_state = 3

                # Spawn the bot with their desired flag
                bot_spawn = subprocess.run(["./spawn_bot.sh", bot_network_name, line], timeout=3, stdout=subprocess.PIPE, check=True, text=True)
                bot_container_id = bot_spawn.stdout.split("\n")[0]
                req.wfile.write(f"[+] Bot spawned using fake flag: {line}\n".encode())

    except Exception as e:
        logger.warning(f"{e}")

    req.request.setblocking(True)
    return bot_container_id

def worker(req: MyTCPHandler):

    ip = req.client_address[0]
    src_port = req.client_address[1]

    if not DEBUG:
        real_ip = req.pp_result.source[0].exploded
    else:
        real_ip = ip
    print(f"Worker {threading.get_ident()} handling real ip {real_ip}")
    req.wfile.write(b"[+] Handling your job now\n")

    id = os.urandom(16).hex()
    path = Path("/tmp") / id
    if not path.exists():
        path.mkdir()

    port = get_port(threading.get_ident())
    instance_idx = port - PORT_BASE

    req.wfile.write(f"\n[*] ip = {MY_IP}\n".encode())
    req.wfile.write(f"[*] port = {port}\n\n".encode())

    timeout = 60 * 5
    req.wfile.write(f"[*] This instance will stay up for {timeout} seconds\n".encode())
    req.wfile.flush()


    start_time = time.time()

    try:
        proc = subprocess.run([
            "./launch.sh",
            IP_BASE.format(instance_idx),
            IFACE.format(instance_idx - 1),
            real_ip,
            CHAL_NET_PREFIX + str(instance_idx),
            CHAL_IMAGE_NAME
        ], stdout=subprocess.PIPE, timeout=3, check=True, text=True)
    except Exception as e:
        req.wfile.write(b"[*] Error\n")
        req.wfile.flush()
        return

    try:
        req.wfile.write(f"\n[!] Instance running!\n".encode())
        req.wfile.write(f"\nOptions:\n".encode())
        req.wfile.write(f"  [1] Launch bot with real flag\n".encode())
        req.wfile.write(f"  [2] Launch bot with custom flag\n".encode())
        req.wfile.write(f"Choice: ".encode())
    except Exception as e:
        pass

    container_id = proc.stdout.split("\n")[0]
    bot_container_id = None

    last_health_check = time.time()

    while time.time() - start_time < timeout:
        try:
            if time.time() - last_health_check > 10:
                status_check = subprocess.run(["./status.sh", container_id], timeout=3)
                if status_check.returncode != 0:
                    logger.warning(f"Container died for {real_ip}")
                    break
                last_health_check = time.time()

            if bot_container_id is None:
                # non-blocking
                bot_container_id = process_command(
                    req,
                    CHAL_NET_PREFIX + str(instance_idx)
                )

            time.sleep(1)

            if is_socket_closed(req.connection):
                logger.warning(f"{real_ip} closed\n")
                break
        except Exception as e:
            logger.warning(str(e))
            raise e
            break

    try:
        kill = subprocess.run(["./kill.sh", container_id], timeout=3)
        if bot_container_id is not None:
            kill = subprocess.run(["./kill.sh", bot_container_id], timeout=3)
    except Exception as e:
        req.wfile.write(b"[*] Error. Please contact admins.\n")
        logger.warning(str(e))
        pass

    req.wfile.write(b"[*] Done. Goodbye!\n")
    req.wfile.flush()

if __name__ == "__main__":
    port = 9000
    MY_IP = requests.get("https://api.ipify.org?format=json").json()['ip']
    with MyTCPServer(("0.0.0.0", port), MyTCPHandler) as server:
        try:
            pool = ThreadPool(processes=NUM_SERVERS)
            print(f"[*] Listening on port {port}")
            server.serve_forever()
        finally:
            pool.close()
