#!/usr/bin/env sage

from common import *
from Crypto.Random import random

import json
import threading
import socket

with open("passwords", 'r') as f:
    passwords = f.read().strip().split('\n')

class Server:
    CHUNK = 64

    def __init__(self, host='0.0.0.0', port=31337):
        print(f"Binding to {host}:{port}")
        self.s = socket.socket()
        self.s.bind((host, port))

    def listen(self):
        self.s.listen(5)
        while True:
            c, addr = self.s.accept()
            threading.Thread(target=self.puzzle, args=(c,)).start()

    def puzzle(self, conn):
        c = conn

        def send(msg):
            c.sendall((msg + '\n').encode())

        def recv():
            message = b''
            while len(message) < 4098:
                part = c.recv(self.CHUNK)
                if b'\n' in part:
                    message += part.split(b'\n')[0]
                    break
                else:
                    message += part
            return message

        try:
            xs = []
            ys = []
            bs = []

            m = xy_to_curve(*json.loads(recv()))

            for i in range(len(passwords)):
                b = sample_R()
                p = b * base_p

                bs.append(b)

                key = F(md5(passwords[i].encode()))

                px, py = p.xy()
                xs.append((key, px))
                ys.append((key, py))

            x_poly = R.lagrange_polynomial(xs)
            y_poly = R.lagrange_polynomial(ys)

            send(str(x_poly))
            send(str(y_poly))

            ks = set(json.loads(recv()))
            if len(ks) > 20:
                send("Error: password limit exceeded.")
                return

            intersection = []
            for p, b in zip(passwords, bs):
                elem = sha(p.encode() + str((b * m)).encode()).hex()
                if elem in ks:
                    intersection.append(p)


            if len(intersection) == len(passwords):
                send("They've all been pwned?! Really?!?! Please hold my flag while I go change them.")
                with open("flag", "r") as f:
                    send(f.read())
            elif len(intersection) != 0:
                send("Some of my passwords have been leaked! I'll change them when I get around to it...")
            else:
                send("It's good to know that none of my passwords are in your pwned database :)")


            c.shutdown(1)
            c.close()
        except Exception as e:
            pass


if __name__ == "__main__":
    server = Server()
    server.listen()

