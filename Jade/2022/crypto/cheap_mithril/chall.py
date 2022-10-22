import random
from Crypto.Util.number import *
from secret import flag

flag = int.from_bytes(flag, "big")

nbits, rbits = 256, 240
e = 65537

while True:
    p = getPrime(nbits)
    q = getPrime(nbits)
    N = p * q
    tot = N + 1 - (p + q)
    if GCD(e, tot) == 1:
        d = inverse(e, tot)
        break

# dirty minerals
x = random.randint(0, 1<<rbits)
y = random.randint(0, 1<<rbits)

# using Valonir's gold n silver
A = pow(p + q * y, x, N)
B = pow(q + p * x, y, N)

# two rings divide
X = pow(e * x + A, 2, N)
Y = pow(e * y + B, 2, N)

# is this mithril?
ct = pow(flag, e, N)
assert pow(ct, d, N) == flag

# 1000 years later...
print(f"N = {N}")
print(f"A = {A}")
print(f"B = {B}")
print(f"X = {X}")
print(f"Y = {Y}")
print(f"ct = {ct}")