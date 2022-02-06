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

class RNG:
    def __init__(self, lfsr, N, nbits):
        self.lfsr = lfsr
        self.N = N
        self.nbits = nbits
        
        if not (pow(2, 27) < N < pow(2, 31)):
            raise ValueError("modulus is too big or small")
        
        K = pow(2, nbits) // N
        self.cutoff = K * N

    def get_random_nbit_integer(self):
        res = 0
        for i in range(self.nbits):
            res += self.lfsr.bit() << i
        return res
    
    def get_random_integer_modulo_N(self):
        count = 1
        while True:
            x = self.get_random_nbit_integer()
            if x < self.cutoff:
                return x % self.N, count
            count += 1

taps = [60, 58, 54, 52, 48, 47, 45, 43, 38, 36, 32, 28, 22, 21, 13, 9, 8, 5, 2, 0]
n = 64

with open("flag.txt", "r") as f:
    flag = f.read()

if __name__ == "__main__":
    print("Welcome to the unbiased random number factory!")
    N = int(input("What modulus would you like to use? Choose between 2^27 and 2^31: "))

    key = secrets.randbits(n)
    key_bits = [(key >> i)&1 for i in range(n)]
    
    lfsr = LFSR(key_bits, taps)
    rng = RNG(lfsr, N, 32)
    
    for _ in range(1024):
        c = input("Enter your command (R,F): ")
        if c.startswith("R"):
            x,t = rng.get_random_integer_modulo_N()
            print("creating this random number took {} attempts".format(t))
        elif c.startswith("F"):
            seed = int(input("what was my seed?"))
            if seed == key:
                print(flag)
            exit(0)
        else:
            print("unsupported command")
