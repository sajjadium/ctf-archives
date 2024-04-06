#!/usr/local/bin/python3

from Crypto.Util.number import *
from math import isqrt

flag = bytes_to_long(open('flag.txt', 'rb').read())
p, q = getPrime(1024), getPrime(1024)
N = p * q
e = getPrime(64)
d = pow(e, -1, N - p - q + 1)

encrypted_flag = pow(flag, e, N)
print(f"{encrypted_flag = }")

try:
    for i in range(10):
        c = int(input("message? "))
        if isqrt(N) < c < N:
            if c == encrypted_flag or c == (N - encrypted_flag):
                print("sorry, that looks like the flag")
                continue
            print(hex(pow(c, d, N))[2:])
        else:
            print("please pick a number which I can (easily) check does not look like the flag.")
except:
    exit()
print("ok bye")
