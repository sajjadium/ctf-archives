# inferior rngs
from random import SystemRandom
random = SystemRandom()
from Crypto.Util.number import getPrime
p = getPrime(64)
class lcg1:
    def __init__(self, n=64):
        self.a = random.randint(1, 2**n)
        self.b = random.randint(1, 2**n)
        self.x = random.randint(1, 2**n)
        self.m = p
    def next(self):
        ret = self.x
        self.x = (self.a * self.x + self.b) % self.m
        return ret

class lcg2:
    def __init__(self, n=64):
        self.lcg = lcg1(n)
        self.x = random.randint(1, 2**n)
        self.b = random.randint(1, 2**n)
        self.m = p
    def next(self):
        self.x = (self.lcg.next() * self.x + self.b) % self.m
        return self.x

lcg = lcg2()
print(p)
for x in range(5):
    print(lcg.next())

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
