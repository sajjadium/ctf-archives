#!/usr/bin/env python3

from Crypto.Util.number import getPrime, inverse, bytes_to_long
import random
from math import gcd

def init():
    p = getPrime(1024)
    q = getPrime(1024)
    return p, q

def new_user(p, q):
    phi = (p - 1) * (q - 1)
    while True:
        e = random.randint(2, 100000)
        if gcd(e, phi) == 1:
            break
    d = inverse(e, phi)
    return e, d

def encrypt(m, e, n):
    return pow(m, e, n)


p, q = init()
n = p * q
e_a, d_a = new_user(p, q)
e_b, d_b = new_user(p, q)

FLAG = b"THC2021{??????????????????????????????????????}"

c = encrypt(bytes_to_long(FLAG), e_b, n)

print(f"The public modulus : {hex(n)}")
print(f"Your key pair : ({hex(e_a)}, {hex(d_a)})")
print(f"Your boss public key : {hex(e_b)}")
print(f"Intercepted message : {hex(c)}")
