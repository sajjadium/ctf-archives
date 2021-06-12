import socket
from socketserver import ThreadingTCPServer, StreamRequestHandler
import time
from email.utils import formatdate
from pathlib import Path
import re
import os

port = 3101

header_template = """HTTP/1.1 {status_code} OK\r
Date: {date}\r
Content-Length: {content_length}\r
Connection: keep-alive\r
Content-Type: text/plain; charset="utf-8"\r
\r
"""

filepath_re = re.compile(r"[^a-z0-9-/]")


def http_header(s: str, status_code: int):
    return header_template.format(
        status_code=status_code,
        date=formatdate(timeval=None, localtime=False, usegmt=True),
        content_length=len(s),
    ).encode()


def client_str(req):
    ip = req.client_address[0]
    port = req.client_address[1]
    return f"{ip}:{port}"


def iter_chunks(xs, n=1448):
    """Yield successive n-sized chunks from xs"""
    for i in range(0, len(xs), n):
        yield xs[i : i + n]


class MyTCPServer(ThreadingTCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 10)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 3)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)
        self.socket.bind(self.server_address)


class TcpHandler(StreamRequestHandler):
    def on_disconnect(self):
        print(f"[*] Disconnected {client_str(self)}")

    def send_401(self):
        error = "Unauthorized"
        self.wfile.write(http_header(error, 401))
        self.wfile.write(error.encode())

    def send_404(self):
        error = "Not Found"
        self.wfile.write(http_header(error, 404))
        self.wfile.write(error.encode())

    def send_file(self, filepath):
        if not filepath.is_file():
            self.send_404()
            return

        content = open(filepath, "rb").read()
        self.wfile.write(http_header(content.decode(), 200))

        for chunk in iter_chunks(content):
            self.wfile.write(chunk)
            time.sleep(0.1)

    def has_token(self):
        ans = False
        while True:
            header = self.rfile.readline().decode().strip()
            if len(header) == 0:
                break
            elif header.startswith("Cookie:"):
                ans = os.environ["TOKEN"] in header

        return ans

    def route_flag(self):
        if self.has_token():
            flag = os.environ["FLAG"]
            self.wfile.write(http_header(flag, 200))
            self.wfile.write(flag.encode())
        else:
            self.send_401()

    def route_note(self, route):
        # Discard the rest of the request
        while len(self.rfile.readline().strip()) != 0:
            pass

        filepath = Path("/tmp/boards") / route
        self.send_file(filepath)

    def handle(self):
        try:
            while True:
                line = self.rfile.readline().strip().decode()
                if len(line) == 0:
                    self.on_disconnect()
                    return

                print(f"[*] {line} {client_str(self)}")

                route = line.split()[1]
                route = filepath_re.sub("", route).strip("/")

                if route == "flag":
                    self.route_flag()
                else:
                    self.route_note(route)

        except ConnectionError as e:
            print(f"[-] {e} {client_str(self)}")
            self.on_disconnect()
            return


if __name__ == "__main__":
    tcp = MyTCPServer(("0.0.0.0", port), TcpHandler)
    print(f"[*] Listening on port {port} ...")
    tcp.serve_forever()
