#!/usr/bin/env python3
from Crypto.Util.number import isPrime, getRandomRange, bytes_to_long
from typing import List
import os, signal


class SecretSharing:
    def __init__(self, p: int, n: int, secret: int):
        self.p = p
        self.n = n
        self.poly = [secret] + [getRandomRange(0, self.p - 1) for _ in range(n - 1)]

    def evaluate(self, x: int) -> int:
        return (
            sum([self.poly[i] * pow(x, i, self.p) for i in range(len(self.poly))])
            % self.p
        )

    def get_shares(self) -> List[int]:
        return [self.evaluate(i + 1) for i in range(self.n)]


if __name__ == "__main__":
    signal.alarm(30)
    secret = bytes_to_long(os.urandom(32))
    while True:
        p = int(input("p = "))
        n = int(input("n = "))
        if isPrime(p) and int(13.37) < n < p:
            shares = SecretSharing(p, n, secret).get_shares()
            print("shares =", shares[:-1])
        else:
            break
    if int(input("secret = ")) == secret:
        print(open("flag.txt", "r").read().strip())
