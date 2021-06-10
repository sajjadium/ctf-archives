import os
import socketserver
import string
import threading
from time import *
import time
import binascii

ROUNDS = 4
BLOCK_SIZE = 8

sbox = [237, 172, 175, 254, 173, 168, 187, 174, 53, 188, 165, 166, 161, 162, 131, 227, 191, 152, 63, 182, 169, 136, 171, 184, 149, 148, 183, 190, 181, 177, 163, 186, 207, 140, 143, 139, 147, 138, 155, 170, 134, 132, 135, 18, 193, 128, 129, 130, 157, 156, 151, 158, 153, 24, 154, 11, 141, 144, 21, 150, 146, 145, 179, 22, 245, 124, 236, 206, 105, 232, 43, 194, 229, 244, 247, 242, 233, 224, 235, 96, 253, 189, 219, 234, 241, 248, 251, 226, 117, 252, 213, 246, 240, 176, 249, 178, 205, 77, 231, 203, 137, 200, 107, 202, 133, 204, 228, 230, 225, 196, 195, 198, 201, 221, 199, 95, 216, 217, 159, 218, 209, 214, 215, 222, 83, 208, 211, 243, 44, 40, 46, 142, 32, 36, 185, 42, 45, 38, 47, 34, 33, 164, 167, 98, 41, 56, 55, 126, 57, 120, 59, 250, 37, 180, 119, 54, 52, 160, 51, 58, 5, 14, 79, 30, 8, 12, 13, 10, 68, 0, 39, 6, 1, 16, 3, 2, 23, 28, 29, 31, 27, 9, 7, 62, 4, 60, 19, 20, 48, 17, 87, 26, 239, 110, 111, 238, 109, 104, 35, 106, 101, 102, 103, 70, 49, 100, 99, 114, 61, 121, 223, 255, 88, 108, 123, 122, 84, 92, 125, 116, 112, 113, 115, 118, 197, 76, 15, 94, 73, 72, 75, 74, 81, 212, 69, 66, 65, 64, 97, 82, 93, 220, 71, 90, 25, 89, 91, 78, 85, 86, 127, 210, 80, 192, 67, 50]
perm = [1, 57, 6, 31, 30, 7, 26, 45, 21, 19, 63, 48, 41, 2, 0, 3, 4, 15, 43, 16, 62, 49, 55, 53, 50, 25, 47, 32, 14, 38, 60, 13, 10, 23, 35, 36, 22, 52, 51, 28, 18, 39, 58, 42, 8, 20, 33, 27, 37, 11, 12, 56, 34, 29, 46, 24, 59, 54, 44, 5, 40, 9, 61, 17]
key = open("flag.txt", "rb").read().strip()

class Service(socketserver.BaseRequestHandler):

    def key_expansion(self, key):
        keys = [None] * 5
        keys[0] = key[0:4] + key[8:12]
        keys[1] = key[4:8] + key[12:16]
        keys[2] = key[0:4] + key[8:12]
        keys[3] = key[4:8] + key[12:16]
        keys[4] = key[0:4] + key[8:12]
        return keys

    def apply_sbox(self, pt):
        ct = b''
        for byte in pt:
            ct += bytes([sbox[byte]])
        return ct

    def apply_perm(self, pt):
        pt = bin(int.from_bytes(pt, 'big'))[2:].zfill(64)
        ct = [None] * 64
        for i, c in enumerate(pt):
            ct[perm[i]] = c
        return bytes([int(''.join(ct[i : i + 8]), 2) for i in range(0, len(ct), 8)])

    def apply_key(self, pt, key):
        ct = b''
        for a, b in zip(pt, key):
            ct += bytes([a ^ b])
        return ct

    def handle(self):
        keys = self.key_expansion(key)
        for i in range(65536):
            pt = os.urandom(8)
            ct = pt
            ct = self.apply_key(ct, keys[0])
            for i in range(ROUNDS):
                ct = self.apply_sbox(ct)
                ct = self.apply_perm(ct)
                ct = self.apply_key(ct, keys[i+1])
            self.send(str((int.from_bytes(pt, 'big'), int.from_bytes(ct, 'big'))))

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

    port = 4004
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
