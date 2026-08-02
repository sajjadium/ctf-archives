from Crypto.Util.number import getPrime
from random import SystemRandom
random = SystemRandom()
n = 64
d = 16
P = getPrime(n)

A = random.getrandbits(n)
B = random.getrandbits(n)
xs = []
class lcg:
    def __init__(self):
        self.a = A
        self.b = B
        self.x = random.getrandbits(n)
        xs.append(self.x)
        self.m = P
    def next(self):
        self.x = (self.a * self.x + self.b) % self.m
        return self.x + random.randint(-P//(2**9) + 1, P//(2**9)) # whats life without a lil error!

lcgs = []
for x in range(d):
    lcgs.append(lcg())

print(f"{P = }\n{xs = }\nout = {[x.next() for x in lcgs]}") # smh ig you can have these

from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes as l2b
from Crypto.Util.Padding import pad
from os import urandom
k = pad(l2b(A**2), 16)
iv = urandom(16)
cipher = AES.new(k, AES.MODE_CBC, iv=iv)
print(f"iv = '{iv.hex()}'")
f = open("flag.txt",'rb').read().strip()
enc = cipher.encrypt(pad(f,16))
print(f"enc = '{enc.hex()}'")
