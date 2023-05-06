#!/usr/bin/python3
from Crypto.Util.number import *
import os

BITS = 512
UPPER_BITS = 296
LOWER_BITS = BITS - UPPER_BITS

UPPER = bytes_to_long(os.urandom(UPPER_BITS // 8)) << LOWER_BITS
FLAG = b'codegate2022{this_is_a_sample_flag}'

def menu1():
    while True:
        lower = bytes_to_long(os.urandom(LOWER_BITS // 8))
        p = UPPER | lower
        if isPrime(p): return lower

def menu2():
    p = UPPER + menu1()
    q = getPrime(512)
    e = 0x10001
    n = p * q
    return n, pow(bytes_to_long(FLAG + b'\x00' + os.urandom(128 - 2 - len(FLAG))), e, n)

while True:
    print("1. Generate 10 random primes (only lower bits)")
    print("2. Encrypt a flag")
    idx = int(input("> "))
    if idx == 1:
        print("How many? (Up to 10)")
        num = int(input("> "))
        for _ in range(min(10, num)):
            print(menu1())
    elif idx == 2:
        n, c = menu2()
        print(f"n : {n}")
        print(f"c : {c}")
UPPER = bytes_to_long(os.urandom(UPPER_BITS // 8)) << LOWER_BITS
