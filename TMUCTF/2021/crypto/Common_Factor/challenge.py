from Crypto.Util.number import *
from functools import reduce


def encrypt(msg, n):
    enc = pow(bytes_to_long(msg), e, n)
    return enc


e = 65537

primes = [getPrime(2048) for i in range(5)]
n = reduce(lambda a, x: a * x, primes, 1)
print(n)

x1 = primes[1] ** 2
x2 = primes[2] ** 2
x3 = primes[1] * primes[2]
y1 = x1 * primes[2] + x2 * primes[1]
y2 = x2 * (primes[3] + 1) - 1
y3 = x3 * (primes[3] + 1) - 1
print(x2 + x3 + y1)
print(y2 + y3)

with open('flag', 'rb') as f:
    flag = f.read()
    print(encrypt(flag, n))
