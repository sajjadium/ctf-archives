#!/usr/bin/env python3

from Crypto.Util.number import *
from secret import C, e, d, p, q, r, flag

O = [1391526622949983, 2848691279889518, 89200900157319, 31337]

assert isPrime(e) and isPrime(d) and isPrime(p) and isPrime(q) and isPrime(r)
assert C[0] * p - C[1] * q >= 0
assert C[2] * q - C[3] * r >= 0
assert C[4] * r - C[5] * p >= 0
assert (C[0] * p - C[1] * q) ** e + (C[2] * q - C[3] * r) ** e + (C[4] * r - C[5] * p) ** e == d * (C[0] * p - C[1] * q) * (C[2] * q - C[3] * r) * (C[4] * r - C[5] * p)
assert C[6] * e - C[7] * d == O[3]

n = e * d * p * q * r
m = bytes_to_long(flag)
c = pow(m, 65537, n)
print(f'C = {C}')
print(f'c = {c}')