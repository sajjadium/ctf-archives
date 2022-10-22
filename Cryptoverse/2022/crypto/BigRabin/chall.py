from Crypto.Util.number import *
from secret import flag
import os, functools

primes = []
e = 2

for _ in range(10):
    primes.append(getPrime(1024))

n = functools.reduce((lambda x, y: x * y), primes)
m = bytes_to_long(os.urandom(256) + flag)
c = pow(m,e,n)

print(primes)
print(c)