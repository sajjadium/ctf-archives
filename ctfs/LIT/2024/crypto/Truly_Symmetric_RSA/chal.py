#!/usr/bin/env python3
from Crypto.Util.number import long_to_bytes as ltb, bytes_to_long as btl, getPrime

p = getPrime(1536)
q = getPrime(1024)

n = p*q

e = p

with open("flag.txt", "rb") as f:
	PT = f.read()

CT = pow(btl(PT), e, n)
print(f"{len(PT) = }")
print(f"{CT = }")
print(f"{n = }")
