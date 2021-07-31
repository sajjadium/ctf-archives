#!/usr/bin/env python

from Crypto.Util.number import *
from flag import FLAG

def nextPrime(n):
    while True:
        n += (n % 2) + 1
        if isPrime(n):
            return n

f = [int(x) for x in bin(int(FLAG.hex(), 16))[2:]]

f.insert(0, 0)
for i in range(len(f)-1): f[i] += f[i+1]

a = nextPrime(len(f))
b = nextPrime(a)

g, h = [[_ for i in range(x) for _ in f] for x in [a, b]]

c = nextPrime(len(f) >> 2)

for _ in [g, h]:
    for __ in range(c): _.insert(0, 0)
    for i in range(len(_) -  c): _[i] += _[i+c]

g, h = [int(''.join([str(_) for _ in __]), 5) for __ in [g, h]]

for _ in [g, h]:
    if _ == g:
        fname = 'g'
    else:
        fname = 'h'
    of = open(f'{fname}.enc', 'wb')
    of.write(long_to_bytes(_))
    of.close()