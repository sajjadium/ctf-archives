from Crypto.Util.number import *
from sympy import nextprime

flag = b'REDACTED'

p = getPrime(1024)
q = nextprime(p)
e = 65537

n = p * q
c = pow(bytes_to_long(flag), e, n)

print(f"n = {n}")
print(f"c = {c}")

