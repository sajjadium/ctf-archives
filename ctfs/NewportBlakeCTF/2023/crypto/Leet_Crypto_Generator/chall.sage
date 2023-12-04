#!/usr/bin/sage
from sage.crypto.util import ascii_to_bin
from Crypto.Util.number import *
import hashlib
import random

print("starting...")

class LCG:
    def __init__(self, seed, p):
        self.seed = seed
        self.p = p
        self.a = random.randint(0,p)
        self.b = random.randint(0,self.a)

    def next(self):
        self.seed = (self.seed*self.a + self.b) % self.p
        return self.seed

p = random_prime(2^256)
a, b = 3, 4
E = EllipticCurve(GF(p), [a,b])
G = E.gens()[0]

lcg = LCG(random.randint(0,p), p)

flag = "nbctf{[REDACTED]}"
flag_bits = list(map(int, list(str(ascii_to_bin(flag)))))

while True:
    inp = int(input("Pick an index of a flag bit: "))
    assert inp >= 0 and inp < len(flag_bits)

    if flag_bits[inp] == 0:
        x = E.random_element()
        print("I wonder what this is: " + str(x.xy()))
    elif flag_bits[inp] == 1:
        x = G*bytes_to_long(flag.encode()) + E.random_element()*int(hashlib.sha256(flag.encode()).hexdigest(), 16)
        y = lcg.next()*x + G*bytes_to_long(flag.encode())
        print("I wonder what this is: " + str(y.xy()))
