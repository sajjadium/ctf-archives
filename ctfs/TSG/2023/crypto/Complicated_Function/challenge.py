from Crypto.Util.number import isPrime, getStrongPrime
from math import isqrt, sin, ceil
from secrets import flag


def f(p):
    return isqrt(p**2 + p * (2**512-6) + ceil(isqrt(p)*sin(p))) + 2**1023


while True:
    p = getStrongPrime(1024)
    if p < 2**1023:
        continue
    q = f(p)
    if isPrime(q):
        break

N = p * q
e = 0x10001
m = int.from_bytes(flag, 'big')
c = pow(m, e, N)

print(f'N = {N}')
print(f'c = {c}')
