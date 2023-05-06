#!/usr/bin/env python3
from Crypto.Util.number import *

FLAG = open('flag.txt', 'rb').read()

bits = 512
e = 65537
p = getPrime(bits)
q = getPrime(bits)
n = p*q
phi = (p-1)*(q-1)
d = inverse(e, phi)
hint = 2*d*(p-1337)

m = bytes_to_long(FLAG)
c = pow(m, e, n)

print(f"n = {hex(n)}")
print(f"e = {hex(e)}")
print(f"c = {hex(c)}")
print(f"hint = {hex(hint)}")
