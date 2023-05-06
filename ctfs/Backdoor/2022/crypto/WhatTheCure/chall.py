#!/usr/bin/python3

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import long_to_bytes
from random import randint
from hashlib import sha256
import json

from secret import p, G, flag

def points_add(P, Q):
    x1, y1 = P
    x2, y2 = Q
    m = (1 - x1 * x2) % p
    x = ((x1 + x2) * pow(m, -1, p)) % p
    y = (y1 * y2 * m * m) % p
    return (x, y)

def point_scalar_mult(P, n):
    R = (0, 1)
    while (n > 0):
        if n & 1: R = points_add(R, P)
        P = points_add(P, P)
        n //= 2
    return R

if __name__ == "__main__":
    k = randint(1, p//2)
    R = point_scalar_mult(G, k)
    key = sha256(long_to_bytes(k)).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    ct = cipher.encrypt(pad(flag, 16)).hex()

    out = {}
    out['Gx'], out['Gy'] = G
    out['Rx'], out['Ry'] = R
    out['ct'] = ct
    
    with open("out.json", "wt") as f:
        f.write(json.dumps(out))

