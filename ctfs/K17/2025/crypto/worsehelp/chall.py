from Crypto.Util.number import isPrime, getStrongPrime
from os import urandom
from math import gcd
from secrets import FLAG

a, b = map(int, input("Enter your secure parameters a, b (as comma-separated values) to seed the RNG: ").split(","))

if a.bit_length() < 1024 or b.bit_length() < 1024 or not isPrime(a) or isPrime(b):
    print("Your parameters are not secure")
    quit()

p, q = getStrongPrime(1024), getStrongPrime(1024)

n = p * q
phi = (p - 1) * (q - 1)


# to harden d
r = ((a**2 + b**2 + 3*a + 3*b + a*b) * pow(2 * a * b + 7, -1, phi)) % phi

while gcd(k := int.from_bytes(urandom(32), "big"), phi) != 1:
    continue

d = pow(k, r, phi)
d |= 1

e = pow(d, -1, phi)

m = int.from_bytes(FLAG, "big")
c = pow(m, e, n)

print(f"{c = }")
print(f"{e = }")
print(f"{n = }")