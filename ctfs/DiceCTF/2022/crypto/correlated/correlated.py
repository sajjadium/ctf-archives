#!/usr/local/bin/python

import secrets

class LFSR:
    def __init__(self, key, taps):
        self._s = key
        self._t = taps            

    def _sum(self, L):
        s = 0
        for x in L:
            s ^= x
        return s

    def _clock(self):
        b = self._s[0]
        self._s = self._s[1:] + [self._sum(self._s[p] for p in self._t)]
        return b

    def bit(self):
        return self._clock()

taps = [45, 40, 39, 36, 35, 34, 33, 32, 30, 28, 27, 23, 22, 21, 19, 17, 16, 15, 14, 13, 9, 7, 3, 0]
n = 48
m = 20000
prob = 0.80
delta = 1048576

with open("flag.txt", "r") as f:
    flag = f.read()

if __name__ == "__main__":
    print("I heard that fast correlation attacks don't work if your LFSR has more than 10 taps.")
    print("You have 60 seconds to recover the key.")

    key = secrets.randbits(n)
    key_bits = [(key >> i)&1 for i in range(n)]
    
    lfsr = LFSR(key_bits, taps)
    stream = [lfsr.bit() for _ in range(m)]

    noise = [secrets.randbelow(delta) > prob * delta for i in stream]
    stream = [i ^ j for i,j in zip(noise, stream)]

    print("Here are {} bits of the stream with {}% accuracy".format(m, 100 * prob))
    print(int("".join(map(str, stream)), 2))

    seed = int(input("what is my key?"))
    if seed == key:
        print(flag)

