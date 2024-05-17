#!/usr/local/bin/python3.10 -u

from Crypto.Util.number import *
import random

a = getRandomNBitInteger(30)
c = getRandomNBitInteger(15)
m = getPrime(32)
x0 = getRandomNBitInteger(30)

n = random.randint(2**8, 2**10)

flag = open("flag.txt").read().strip()

class Random():
    global m, a, c

    def __init__(self, x0):
        self.x0 = x0

    def random(self):
        self.x0 = (a*self.x0+c) % m
        return self.x0


encryptor = Random(x0)

assert m < 2**32
assert isPrime(m)

x = [ord(i) for i in flag]

with open("out.txt", "w") as wfile:
    for ind in range(len(x)):
        next = encryptor.random()
        if ind < 6:
            print(str(next))
            wfile.write(str(next) + "\n")
        for __ in range(n-1):
            x[ind] ^= encryptor.random()
    print(f"n = {n}")
    print(" ".join([str(i) for i in x]))
    wfile.write("n = " + str(n) + "\n")
    wfile.write(" ".join([str(i) for i in x]) + "\n")
