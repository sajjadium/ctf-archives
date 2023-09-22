#!/usr/bin/env python3

from Crypto.Util.number import *
from flag import flag

def gen_prime(nbit):
	while True:
		p = 0
		for i in range(nbit, nbit>>1, -1):
			p += getRandomRange(0, 2) * 2 ** i
		p += getRandomNBitInteger(nbit>>3)
		if isPrime(p):
			return p

nbit = 512
p, q, r = [gen_prime(nbit) for _ in '012']
e, n = 65537, p * q * r

m = bytes_to_long(flag)
c = pow(m, e, n)

print(f'n = {n}')
print(f'c = {c}')