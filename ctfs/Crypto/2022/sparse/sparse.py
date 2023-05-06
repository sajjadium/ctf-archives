#!/usr/bin/env python3

from Crypto.Util.number import *
from flag import flag

def sparse(p, k):
	nbit = p.bit_length()
	while True:
		CF = [getRandomRange(-1, 1) for _ in '_' * k]
		XP = [getRandomRange(3, nbit - 3) for _ in '_' * k]
		A = sum([CF[_] * 2 ** XP[_] for _ in range(0, k)])
		q = p + A
		if isPrime(q) * A != 0:
			return q

p = getPrime(417)
q = sparse(p, 5)
e, n = 65537, p * q
print(f'n = {n}')
m = bytes_to_long(flag.encode('utf-8'))
assert m < n
c = pow(m, e, n)
print(f'c = {c}')
