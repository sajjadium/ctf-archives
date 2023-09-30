import hashlib
import random
import string
import socket
from socketserver import ThreadingTCPServer, StreamRequestHandler
from multiprocessing import TimeoutError
from multiprocessing.pool import ThreadPool
import threading
import subprocess
import os
import base64
from pathlib import Path
import shutil
import requests
from proxyprotocol.v2 import ProxyProtocolV2
from proxyprotocol.reader import ProxyProtocolReader
from proxyprotocol import ProxyProtocolWantRead
from pow import get_challenge, verify_challenge, SOLVER_URL

PORT_BASE = int(os.getenv("CHALL_PORT_BASE", "7000"))
IP_BASE = "10.0.4."
POW_DIFFICULTY = int(os.getenv("POW_DIFFICULTY", "0"))
NUM_SERVERS = int(os.getenv("CHALL_NUM_SERVERS", "5"))
DEBUG = int(os.getenv("DEBUG", "0")) == 1
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
    except Exception as e:
        logger.exception("unexpected exception when checking if a socket is closed")
        return False
    return False

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

    req.wfile.write(f"\n[*] ip = {MY_IP}\n".encode())
    req.wfile.write(f"[*] port = {port}\n\n".encode())

    timeout = 60 * 5
    req.wfile.write(f"[*] This instance will stay up for {timeout} seconds\n".encode())
    req.wfile.flush()

    proc = subprocess.Popen(["/nsjail.sh", IP_BASE+str(port - PORT_BASE), real_ip], stdout=req.wfile)
    for x in range(timeout // 5):
        try:
            proc.wait(5)
            break
        except subprocess.TimeoutExpired:
            if is_socket_closed(req.request):
                break

    proc.terminate()
    try:
        proc.wait(1)
    except subprocess.TimeoutExpired:
        proc.kill()

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
