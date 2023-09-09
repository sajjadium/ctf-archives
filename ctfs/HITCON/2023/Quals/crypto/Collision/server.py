#!/usr/bin/env python3
import os
import signal

if __name__ == "__main__":
    salt = os.urandom(8)
    print("salt:", salt.hex())
    while True:
        m1 = bytes.fromhex(input("m1: "))
        m2 = bytes.fromhex(input("m2: "))
        if m1 == m2:
            continue
        h1 = hash(salt + m1)
        h2 = hash(salt + m2)
        if h1 == h2:
            exit(87)
        else:
            print(f"{h1} != {h2}")
