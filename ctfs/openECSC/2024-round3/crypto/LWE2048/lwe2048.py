#!/usr/bin/env python3

import os
from secrets import randbelow, randbits

flag = os.getenv('FLAG', 'flag{redacted}')

class Chall:
    def __init__(self, nbits=2048):
        self.n = randbits(nbits)
        self.s = [randbelow(self.n) for _ in range(4)]
        self.B = self.n // (3*nbits)
    
    def query(self, x):
        res = randbelow(self.B)
        assert len(x) == 4
        assert all((xi % self.n) != 0 for xi in x)
        for si, xi in zip(self.s, x):
            res = (res + si*xi) % self.n
        return res


def main():
    print("I'm gonna send you a bunch of random numbers. But you can choose how random!")

    chall = Chall()
    print(f"The modulus is {chall.n}")

    for _ in range(10000):
        x = list(map(int, input("> ").strip().split(",")))
        y = chall.query(x)
        print(y)
    
    guess = input("What's your guess? ")
    if guess == ",".join(map(str, chall.s)):
        print(flag)


if __name__ == "__main__":
    main()
