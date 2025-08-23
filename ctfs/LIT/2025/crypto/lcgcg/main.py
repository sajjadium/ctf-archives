#!/usr/bin/env python3
# inferior rngs
from random import SystemRandom
random = SystemRandom()
from Crypto.Util.number import getPrime
p = getPrime(64)
class LCG:
    def __init__(self, a, b, x):
        self.a = a
        self.b = b
        self.x = x
        self.m = p
    def next(self):
        self.x = (self.a * self.x + self.b) % self.m
        ret = self.x
        return ret

class LCG2:
    def __init__(self, baselcg, n=100):
        self.lcg = baselcg
        for i in range(n):
            a = self.lcg.next()
            b = self.lcg.next()
            x = self.lcg.next()
            self.lcg = LCG(a,b,x)
    def next(self):
        return self.lcg.next()

a = random.randint(1, 2**64)
b = random.randint(1, 2**64)
x = random.randint(1, 2**64)
lcg = LCG(a, b, x)
lcg2 = LCG2(lcg)
print(p)
for x in range(3):
    print(lcg2.next())

from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes as l2b
from Crypto.Util.Padding import pad
from os import urandom
r = lcg.next()
k = pad(l2b(r**2), 16)
iv = urandom(16)
cipher = AES.new(k, AES.MODE_CBC, iv=iv)
print(iv.hex())
f = open("flag.txt",'rb').read().strip()
enc = cipher.encrypt(pad(f,16))
print(enc.hex())
