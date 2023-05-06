#!/usr/bin/env python3

from Crypto.Util.number import *
import random
import os
from flag import flag

def urand(b):
    return int.from_bytes(os.urandom(b), byteorder='big')

class PRNG:
    def __init__(self):
        self.m1 = 2 ** 32 - 107
        self.m2 = 2 ** 32 - 5
        self.m3 = 2 ** 32 - 209
        self.M = 2 ** 64 - 59

        rnd = random.Random(b'rbtree')

        self.a1 = [rnd.getrandbits(20) for _ in range(3)]
        self.a2 = [rnd.getrandbits(20) for _ in range(3)]
        self.a3 = [rnd.getrandbits(20) for _ in range(3)]

        self.x = [urand(4) for _ in range(3)]
        self.y = [urand(4) for _ in range(3)]
        self.z = [urand(4) for _ in range(3)]

    def out(self):
        o = (2 * self.m1 * self.x[0] - self.m3 * self.y[0] - self.m2 * self.z[0]) % self.M

        self.x = self.x[1:] + [sum(x * y for x, y in zip(self.x, self.a1)) % self.m1]
        self.y = self.y[1:] + [sum(x * y for x, y in zip(self.y, self.a2)) % self.m2]
        self.z = self.z[1:] + [sum(x * y for x, y in zip(self.z, self.a3)) % self.m3]

        return o.to_bytes(8, byteorder='big')

if __name__ == "__main__":
    prng = PRNG()

    hint = b''
    for i in range(12):
        hint += prng.out()
    
    print(hint.hex())

    assert len(flag) % 8 == 0
    stream = b''
    for i in range(len(flag) // 8):
        stream += prng.out()
    
    out = bytes([x ^ y for x, y in zip(flag, stream)])
    print(out.hex())
    
