from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hashlib
import secrets
import random

FLAG = open('flag.txt','rb').read()
class LFSR:
    def __init__(self, seed):
        self.state = list(map(int, list(f"{seed:0128b}")))
        self.taps = [0, 16, 32, 64, 96, 127]

    def get(self):
        next_bit = 0
        for tap in self.taps:
            next_bit ^= self.state[tap]
        self.state = self.state[1:] + [next_bit]
        return next_bit

class LCG:
    def __init__(self, seed):
        self.a = 3
        self.b = 7
        self.m = 2**64-59
        self.state = seed % self.m

    def get(self):
        self.state = (self.a * self.state + self.b) % self.m
        out = 1 if self.state >> 58 else 0
        return out


class nonsense: 
    def __init__(self, seed):
        self.lfsr = LFSR(seed)
        self.lcg = LCG(seed)
    
    def get(self):
        t1 = self.lfsr.get()
        t2 = self.lcg.get()
        return t1 ^ t2 ^ 1 

l = 128
key = secrets.randbelow(2**l-1)
prng = nonsense(key)


for i in range(300):
    out = [prng.get() for _ in range(12)]    
    p = getPrime(256)
    
    leak = []
    for x in out:
        if x:
            a = secrets.randbelow(2**180)
            b = secrets.randbelow(a)
            leak.append(a*p + b)
        else:
            leak.append(secrets.randbelow(2**436))

    random.shuffle(leak)
    print(leak)

print(AES.new(hashlib.sha256(long_to_bytes(key)).digest(), AES.MODE_ECB).encrypt(pad(FLAG, 16)).hex())