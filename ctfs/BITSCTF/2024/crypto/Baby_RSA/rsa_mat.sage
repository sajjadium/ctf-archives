#!/usr/bin/env python3

from Crypto.Util.number import bytes_to_long
from Crypto.PublicKey import RSA
from sage.all import matrix, Zmod


key = RSA.generate(2048)

print(f'n = {key.n}')
print()

pt = b'REDACTED'

pt = [bytes_to_long(pt[p:p+len(pt)//4]) for p in range(0, len(pt), len(pt)//4)]

g = matrix(Zmod(key.n), [[pt[0], pt[1]], [pt[2], pt[3]]])


def encrypt(g):
    return g ^ 65537


c = encrypt(g)

for i in c:
    for j in i:
        print(j)
