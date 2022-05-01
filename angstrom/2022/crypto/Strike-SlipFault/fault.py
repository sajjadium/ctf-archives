#!/usr/local/bin/python3

from Crypto.Util.number import getStrongPrime, long_to_bytes, bytes_to_long, inverse
from secrets import randbelow, token_bytes

print("Welcome to my super secret service! (under construction)")

BITS = 4096

p = getStrongPrime(BITS//2)
q = getStrongPrime(BITS//2)
n = p*q
phi = (p-1)*(q-1)
e = 65537

flag = [REDACTED]
m = bytes_to_long(flag+token_bytes(BITS//8 - len(flag) - 1))
c = pow(m,e,n)

print("Making sure nothing was tampered with...")
print("n =", n)
print("e =", e)
print("c =", c)

d = inverse(e, phi)
bits = list(range(d.bit_length()))
for i in range(3):
	d ^= 1 << bits.pop(randbelow(len(bits))) # these cosmic rays man...

ans = long_to_bytes(pow(c,d,n))
if ans.startswith(flag):
	print("Check passed!")
print(f"Check failed, {ans} does not start with the flag.")