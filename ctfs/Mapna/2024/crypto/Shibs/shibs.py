#!/usr/bin/env python3

from Crypto.Util.number import *
from flag import flag

def shift(s, B):
	assert s < len(B)
	return B[s:] + B[:s]

def gen_key(nbit):
	while True:
		p = getPrime(nbit)
		B = bin(p)[2:]
		for s in range(1, nbit):
			q = int(shift(s, B), 2)
			if isPrime(q):
				n = p * q
				return n, p, s

nbit = 1024
n, p, _ = gen_key(nbit)
q = n // p
dna = p & q
m = bytes_to_long(flag)
c = pow(m, 65537, n)

print(f'n = {n}')
print(f'dna = {dna}')
print(f'enc = {c}')
