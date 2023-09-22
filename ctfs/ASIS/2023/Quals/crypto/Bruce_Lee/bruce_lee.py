#!/usr/bin/env python3

from Crypto.Util.number import *
from gmpy2 import *
from flag import flag

def gen_prime(nbit, density):
	while True:
		rar = [2 ** getRandomRange(1, nbit - 1) for _ in range(density)]
		p = sum(rar) + 2**(nbit - 1) + 2**(nbit - 2) + 1
		if isPrime(p):
			return p

nbit, density = 1024, getRandomRange(63, 114)
p, q = [gen_prime(nbit, density) for _ in '01']

e = next_prime(p ^ q + 2**density + 1)

pkey = [e, p * q]

def encrypt(m, pkey):
	e, n = pkey
	c = pow(m, e, n)
	return c

m = bytes_to_long(flag)
c = encrypt(m, pkey)

print(f'n = {p * q}')
print(f'c = {c}')