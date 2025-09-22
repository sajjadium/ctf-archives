#!/usr/bin/python3

import math
import signal
import sys

from Crypto.Util.number import getPrime, inverse, getRandomRange

N_BITS = 512

class A:
    def __init__(self, bits = N_BITS):
        self.p = getPrime(bits // 2)
        self.q = getPrime(bits // 2)
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = 0x10001
        self.d = pow(self.e, -1, self.phi)


    def encrypt(self, m):
        return pow(m, self.e, self.n)


    def decrypt(self, c):
        return pow(c, self.d, self.n)


class B:
    def __init__(self, bits = N_BITS):
        self.p = getPrime(bits // 2)
        self.q = getPrime(bits // 2)
        self.n = self.p * self.q
        self.n_sq = self.n * self.n
        self.g = self.n + 1
        self.lam = (self.p - 1) * (self.q - 1) // math.gcd(self.p - 1, self.q - 1)
        x = pow(self.g, self.lam, self.n_sq)
        L = (x - 1) // self.n
        self.mu = inverse(L, self.n)


    def encrypt(self, m):
        r = getRandomRange(1, self.n)
        while math.gcd(r, self.n) != 1:
            r = getRandomRange(1, self.n)
        c1 = pow(self.g, m, self.n_sq)
        c2 = pow(r, self.n, self.n_sq)
        return (c1 * c2) % self.n_sq


    def decrypt(self, c):
        x = pow(c, self.lam, self.n_sq)
        L = (x - 1) // self.n
        return (L * self.mu) % self.n


def err(msg):
    print(msg)
    exit(1)


def compute(e_secret, xs, a, b):
    ret = 1
    for x in xs:
        ret *= a.encrypt(b.decrypt(e_secret * x))
        ret %= a.n
    return ret


def ans(secret, qs, a, b):
    e_secret = b.encrypt(secret + 0xD3ADC0DE)
    for i in range(7):
        li = qs[i][:len(qs[i]) // 2]
        ri = qs[i][len(qs[i]) // 2:]

        print(f"{compute(e_secret, li, a, b)} {compute(e_secret, ri, a, b)}")


def test(t):
    print(f"--- Test #{t} ---")
    a = A()
    b = B()
    print(f"n = {b.n}")
    print("You can ask 7 questions:")

    qs = []
    for _ in range(7):
        l = list(map(int, input().strip().split()))
        if len(l) % 2 != 0:
            err("You must give me an even number of numbers!")
        if len(l) != len(set(l)):
            err("All numbers must be distinct!")
        qs.append(l)

    secret = getRandomRange(0, 2048)
    ans(secret, qs, a, b)

    print("Can you guess my secret?")
    user = int(input())

    if user != secret:
        err("Seems like you can't")
    else:
        print("Correct!")


def timeout_handler(signum, frame):
    print("Timeout!")
    sys.exit(1)

def main():
    signal.signal(signal.SIGALRM, timeout_handler)

    for i in range(10):
        test(i)

    flag = open('flag.txt', "r").read()
    print(f"Here you go: {flag}")

if __name__ == '__main__':
    main()
