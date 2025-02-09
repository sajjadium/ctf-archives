#!/usr/local/bin/python3

from secrets import randbits
from Crypto.Util.number import isPrime


class LCG:

    def __init__(self, a: int, c: int, m: int, seed: int):
        self.a = a
        self.c = c
        self.m = m
        self.state = seed

    def next(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state


while True:
    a = randbits(512)
    c = randbits(512)
    m = 1 << 512
    seed = randbits(512)
    initial_iters = randbits(16)
    # https://en.wikipedia.org/wiki/Linear_congruential_generator#m_a_power_of_2,_c_%E2%89%A0_0
    if (c != 0 and c % 2 == 1) and (a % 4 == 1):
        print(f"LCG coefficients:\na={a}\nc={c}\nm={m}")
        break

L = LCG(a, c, m, seed)
for i in range(initial_iters):
    L.next()

P = []
while len(P) < 2:
    test = L.next()
    if isPrime(test):
        P.append(test)

p, q = P

n = p * q

t = (p - 1) * (q - 1)

e = 65537

d = pow(e, -1, t)

message = int.from_bytes(open("flag.txt", "rb").read(), "big")

ct = pow(message, e, n)

print(f"n={n}")
print(f"ct={ct}")
