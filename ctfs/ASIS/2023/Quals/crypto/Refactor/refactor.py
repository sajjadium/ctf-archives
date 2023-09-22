#!/usr/bin/env python3

from Crypto.Util.number import *
from flag import flag

def pgen(nbit):
	x, y = 0, 1
	while True:
		u, v = getRandomRange(1, 110), getRandomRange(1, 313)
		x, y = u * x + 31337 * v * y, v * x - u * y
		if x.bit_length() <= nbit // 2 and x.bit_length() <= nbit // 2:
			p = x**2 + 31337 * y**2 | 1
			if isPrime(p) and p.bit_length() >= nbit:
				return p
		else:
			x, y = 0, 1

def encrypt(msg, pkey):
	e, n = pkey
	m = bytes_to_long(msg)
	c = pow(m, e, n)
	return c

p, q = [pgen(1024) for _ in '__']
pkey = (31337, p * q)

c = encrypt(flag, pkey)

print(f'n = {p * q}')
print(f'c = {c}')