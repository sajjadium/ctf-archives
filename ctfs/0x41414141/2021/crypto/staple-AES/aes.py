import os
import socketserver
import string
import threading
from time import *
import random
import time
import binascii

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

iv = b''
key = b''
flag = open("flag.txt", "rb").read().strip()

class Service(socketserver.BaseRequestHandler):

    def handle(self):
        assert len(flag) % 16 == 1
        blocks = self.shuffle(flag)
        ct = self.encrypt(blocks)
        self.send(binascii.hexlify(ct))

    def byte_xor(self, ba1, ba2):
        return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

    def encrypt(self, blocks):
        curr = iv
        ct = []
        cipher = AES.new(key, AES.MODE_ECB)
        for block in blocks:
            curr = cipher.encrypt(curr)
            ct.append(self.byte_xor(block, curr))
        return b''.join(ct)

    def shuffle(self, pt):
        pt = pad(pt, 16)
        pt = [pt[i: i + 16] for i in range(0, len(pt), 16)]
        random.shuffle(pt)
        return pt

    def send(self, string, newline=True):
        if type(string) is str:
            string = string.encode("utf-8")

        if newline:
            string = string + b"\n"
        self.request.sendall(string)

    def receive(self, prompt="> "):
        self.send(prompt, newline=False)
        return self.request.recv(4096).strip()


class ThreadedService(
    socketserver.ThreadingMixIn,
    socketserver.TCPServer,
    socketserver.DatagramRequestHandler,
):
    pass


def main():

    port = 3167
    host = "0.0.0.0"

    service = Service
    server = ThreadedService((host, port), service)
    server.allow_reuse_address = True

    server_thread = threading.Thread(target=server.serve_forever)

    server_thread.daemon = True
    server_thread.start()

    print("Server started on " + str(server.server_address) + "!")

    # Now let the main thread just wait...
    while True:
        sleep(10)


if __name__ == "__main__":
    main()