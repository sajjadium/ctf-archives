import os
from random import shuffle
from math import prod
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from secret import FLAG

class LFSR:
    def __init__(self, state, taps):
        self.state = state
        self.taps = [len(state) - t for t in taps]

    def clock(self):
        out = self.state[0]
        self.state = self.state[1:] + [sum(self.state[t] for t in self.taps)%2]
        return out

class Generator:
    def __init__(self, seed):
        self.seed = list(map(int, bin(seed)[2:].zfill(128)))
        self.lfsr = LFSR(self.seed, [128, 126, 101, 99])
        self.vars = [9, 31, 32, 47, 79, 127] 
        self.mono = [[0, 1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [0], [0, 1, 2, 3, 5], [1], [0, 1, 2, 5], [3], [1, 2, 3, 4], [2], [0, 1, 3, 4]]
    
    def clock(self):
        b = [self.lfsr.state[i] for i in self.vars]
        out = sum(prod(b[i] for i in j) for j in self.mono)
        self.lfsr.clock()
        return out % 2

def encrypt(ptxt, key):
    iv = os.urandom(16)
    cipher = AES.new(key, 2, iv)
    ctxt = cipher.encrypt(pad(ptxt, 16))
    return (iv + ctxt).hex()

key = os.urandom(16)

G = Generator(int.from_bytes(key, 'big'))
resG = [G.clock() for i in range(696)]

resL = []
L = LFSR(resG[:69], [69, 67, 64, 63])
for _ in range(69):
    out = [L.clock() for _ in range(69)]; shuffle(out)
    resL += out

with open('enc', 'w') as f:
    print(resL, file=f)
    print(resG[69:], file=f)
    print(encrypt(FLAG, key), file=f)