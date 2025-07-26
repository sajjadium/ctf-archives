from Crypto.Util.number import *
from secret import FLAG

p, q, r, s = [getPrime(512) for _ in "1234"]

print(f"h1 = {p + q + r + s}")
print(f"h2 = {p**2 + q**2 + r**2 + s**2}")
print(f"h3 = {p**3 + q**3 + r**3 + s**3}")

N = p*q*r*s
print(f"N = {N}")
pt = bytes_to_long(FLAG)
ct = pow(pt, 65537, N)
print(f"ct = {ct}")

