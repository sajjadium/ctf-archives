#!/usr/bin/env python3
from Crypto.Util.number import getPrime, bytes_to_long as btl
from Crypto.Util.Padding import pad as hashing
from flag import flag

p = getPrime(1024)
q = getPrime(1024)
n = p*q
e = 65537
t = (p-1)*(q-1)
d = pow(e, -1, t)

print(f"{e = }")
print(f"{n = }")

flag = flag.encode()
enc = pow(btl(flag), e, n)
print(f"{enc = }")

sign = pow(btl(hashing(flag, 256)), d, n)
print(f"{sign = }")
