#!/usr/bin/env python3

from Crypto.Util.number import bytes_to_long, long_to_bytes
from nsa_ecc_secret import P, Q
import os

flag = b'REDACTED'

s = bytes_to_long(os.urandom(16))


def generate(P, Q, s):
    while True:
        r = int((s * P).x)
        yield from long_to_bytes((r * Q).x)[2:]
        s = int((r * P).x)


g = generate(P, Q, s)


def encrypt(g, t):
    out = []
    for b in t:
        x = next(g)
        out.append(b ^ x)
    return bytes(out)


print(f'P = {P.xy}')
print(f'Q = {Q.xy}')


print(encrypt(g, b'This is a test string for debugging'))

print(encrypt(g, flag))
