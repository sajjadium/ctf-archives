import hashlib
import random
import string
import socket
from socketserver import ThreadingTCPServer, StreamRequestHandler
from multiprocessing import TimeoutError
from multiprocessing.pool import ThreadPool
import threading
import subprocess


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
            if not send_pow(self):
                return

            res = pool.apply_async(worker, (self,))
            pos = pool._inqueue.qsize()  # type: ignore
            self.wfile.write(f"[*] Queued in position {pos}\n".encode())
            res.get(timeout=180)

        except (ConnectionError, TimeoutError):
            pass


def send_pow(req: MyTCPHandler):
    pool = string.ascii_letters + string.digits
    s = "".join(random.choices(pool, k=16))
    h = hashlib.sha256(s.encode()).hexdigest()
    prefix = s[:4]
    suffix = s[4:]
    req.wfile.write(f"[*] suffix = {suffix}\n".encode())
    req.wfile.write(f"[*] sha256 = {h}\n".encode())
    req.wfile.write(f"[*] Give me the {len(prefix)} character prefix: ".encode())
    p = req.rfile.readline().strip().decode("ascii", errors="ignore")
    if p == prefix:
        return True
    else:
        req.wfile.write(f"[-] That's wrong\n".encode())
        return False


def worker(req: MyTCPHandler):
    ip = req.client_address[0]
    port = req.client_address[1]
    print(f"Worker {threading.get_ident()} handling {ip}:{port}")
    req.wfile.write(b"[+] Handling your job now\n")

    popen = subprocess.Popen(
        ["/usr/bin/python3", "-u", "/opt/app/session.py"],
        stdin=req.rfile,
        stdout=req.wfile,
        stderr=req.wfile,
        encoding="utf-8",
        bufsize=0,
    )
    popen.wait()


if __name__ == "__main__":
    port = 9000
    with MyTCPServer(("0.0.0.0", port), MyTCPHandler) as server:
        try:
            pool = ThreadPool(processes=4)
            print(f"[*] Listening on port {port}")
            server.serve_forever()
        finally:
            pool.close()
