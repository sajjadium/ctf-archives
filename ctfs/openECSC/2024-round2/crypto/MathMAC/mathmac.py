#!/usr/bin/env python3

import os
from random import randint
import json

flag = os.getenv('FLAG', 'flag{redacted}')

class MAC:
    def __init__(self, n):
        self.p = 8636821143825786083
        self.n = n
        self.sk = [randint(0, self.p) for _ in range(n)]
        self.base = pow(4, randint(0, self.p), self.p)
    
    def sign(self, x):
        if x < 0 or x >= 2**self.n:
            return None
        x = list(map(int, bin(x)[2:].zfill(self.n)))
        assert len(x) == self.n
        res = self.base
        for ai, xi in zip(self.sk, x):
            if xi == 1:
                res = pow(res, ai, self.p)
        return res


def menu():
    print("1. Generate token")
    print("2. Validate token")
    print("3. Quit")
    return int(input("> "))


def main():
    print("Welcome to the magic MathMAC. Can you become a wizard and guess tokens?")
    M = 64
    mac = MAC(M)
    data = []
    while True:
        choice = menu()
        if choice == 1:
            x = randint(0, 2**M-1)
            data.append(x)
            tag = mac.sign(x)
            print(f"{x},{tag}")
        elif choice == 2:
            x, tag = input().strip().split(",")
            x = int(x)
            tag = int(tag)
            actual_tag = mac.sign(x)
            if actual_tag is None or tag != actual_tag:
                print("Unlucky")
                exit(1)

            if x in data:
                print("Yup. I know.")
            else:
                print(flag)
        else:
            exit(0)


if __name__ == "__main__":
    main()
