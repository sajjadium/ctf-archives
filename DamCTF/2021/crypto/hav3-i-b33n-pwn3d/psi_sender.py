#!/usr/bin/env sage

from common import *
import json
import socket
import sys

IP = "hav3-i-b33n-pwn3d.damctf.xyz"
PORT = 30944

CHUNK = 64

def send(c, msg):
    c.sendall((msg + '\n').encode())

def recv(c):
    message = b''
    while len(message) < 4098:
        part = c.recv(CHUNK)
        if b'\n' in part:
            message += part.split(b'\n')[0]
            break
        else:
            message += part
    return message.decode()


def main():
    passwords = sys.argv[1:]

    a = sample_R()
    m = a*base_p

    s = socket.socket()
    s.connect((IP, PORT))

    send(s, str(list(m.xy())))

    x_poly = R(recv(s))
    y_poly = R(recv(s))

    if x_poly.degree() < 1 or y_poly.degree() < 1:
        exit(1)


    ks = []
    for pas in passwords:
        key = F(md5(pas.encode()))

        px = x_poly(key)
        py = y_poly(key)

        point = xy_to_curve(px, py)

        k = sha((pas + str(a * point)).encode())

        ks.append(k.hex())

    crypt_random.shuffle(ks)

    send(s, json.dumps(ks))

    print(recv(s))


if __name__ == "__main__":
    main()
