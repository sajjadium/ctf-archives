#!/usr/local/bin/python3

import os
from random import Random
import signal

TIMEOUT = 60

FLAG = open("flag.txt", "r").read().strip()


def handle():
    s1 = os.urandom(10)
    r1 = Random(s1)
    len_seed = r1.randint(100, 1200)
    seed = int.from_bytes(os.urandom(len_seed), 'big')

    r2 = Random(seed)
    check = r2.getrandbits(32)
    for _ in range(2000):
        K = bin(int.from_bytes(os.urandom(4), 'big'))[2:].zfill(32)
        V = bin(r2.getrandbits(32))[2:].zfill(32)
        R = [v if k == "1" else "?" for k, v in zip(K, V)]
        print("".join(R))

    print("Enter first 32 bits generated")
    check2 = int(input())
    if check2 == check:
        print("Correct")
    else:
        print("Wrong")
        return
    print("Enter the seed")

    seed2 = int(input(), 16)
    if seed == seed2:
        print("You got it!")
        print(FLAG)
    else:
        print("Wrong seed")


if __name__ == '__main__':
    signal.alarm(TIMEOUT)
    handle()
