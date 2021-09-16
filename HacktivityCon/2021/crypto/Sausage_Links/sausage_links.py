#!/usr/bin/env python3

from gmpy import *
from Crypto.Util.number import *
import gensafeprime

flag = open("flag.txt", "rb").read().strip()

bits = 512

p = getPrime(bits)
q = getPrime(bits)
r = getPrime(bits)
n = p * q * r
phi = (p - 1) * (q - 1) * (r - 1)

l = min([p, q, r])
d = getPrime(1 << 8)
e = inverse(d, phi)

a = gensafeprime.generate(2 * bits)
while True:
    g = getRandomRange(2, a)
    if pow(g, 2, a) != 1 and pow(g, a // 2, a) != 1:
        break

pubkey = (n, e, a, g)

m = bytes_to_long(flag)
k = getRandomRange(2, a)
K = pow(g, k, a)
c1, c2 = pow(k, e, n), (m * K) % a

print("c =", (c1, c2))
print("pubkey =", pubkey)
