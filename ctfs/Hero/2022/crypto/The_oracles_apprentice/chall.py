#!/usr/bin/env python3
from Crypto.Util.number import getStrongPrime, bytes_to_long
import random

FLAG = open('flag.txt','rb').read()

encrypt = lambda m: pow(m, e, n)
decrypt = lambda c: pow(c, d, n)

e = random.randrange(3, 65537, 2)
p = getStrongPrime(1024, e=e)
q = getStrongPrime(1024, e=e)

n = p * q
φ = (p-1) * (q-1)

d = pow(e, -1, φ)

c = encrypt(bytes_to_long(FLAG))

#print(f"{n=}")
#print(f"{e=}")
print(f"{c=}")

for _ in range(3):
     t = int(input("c="))
     print(decrypt(t)) if c != t else None
