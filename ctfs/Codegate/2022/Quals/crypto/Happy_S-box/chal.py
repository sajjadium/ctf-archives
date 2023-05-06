#!/usr/bin/python3
import os
import random

class LFSR:
    rand = random.Random("Codegate2022")
    Sbox = [ [0] * 64 + [1] * 64 for _ in range(512 - 6) ]
    for i in range(len(Sbox)):
        rand.shuffle(Sbox[i])

    def __init__(self, seed):
        self.state = seed
        for _ in range(1024):
            self.next()
    
    def next(self):
        v = self.state
        # x^512 + x^8 + x^5 + x^2 + 1
        n = ((v >> 0) ^ (v >> 504) ^ (v >> 507) ^ (v >> 509)) & 1
        self.state = (v >> 1) | (n << 511)
    
    def output(self):
        out = 0
        for i in range(512 - 6):
            out ^= self.Sbox[i][(self.state >> i) & 127]
        return out


guess_this = os.urandom((512 - 8) // 8)
guess_this = guess_this[:-1] + bytes([guess_this[-1] & 0xf0])
seed = int.from_bytes(guess_this, 'big') << 8
print("Seed generated. It'll take some time to generate a hint.")

v = 0
for i in range(2 ** 12):
    lfsr = LFSR(seed | i)
    v <<= 1
    v |= lfsr.output()

print("Here's the hint. It should be enough.")
print(v.to_bytes(2 ** 12 // 8, 'big').hex())
ans = input("Guess the seed > ")

if guess_this == bytes.fromhex(ans):
    with open('flag', 'r') as f:
        print(f.read())
else:
    print("WRONG")

