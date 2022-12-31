#!/usr/bin/env python3

from Crypto.Util.number import *
from flag import flag

def gen_rhyton(nbit, delta, L):

	p, q = [getPrime(nbit) for _ in '01']
	n = p * q
	D = int(n ** (1 - delta))	
	phi = (p - 1) * (q - 1)

	V = [getRandomRange(1, n - 1) for _ in range(L)]
	U = [phi * v // n for v in V]

	W, i = [], 0
	while True:
		w = getRandomRange(phi * V[i] - U[i] * n - D, phi * V[i] - U[i] * n + D)
		if abs(phi * V[i] - U[i] * n - w) < D and w < n:
			W.append(w)
			i += 1
		if i == L:
			break
	return (p, q, U, V, W)

def encrypt(msg, p, q):
	m, n = bytes_to_long(msg), p * q
	assert m < p * q
	e = 65537
	return pow(m, e, n)

nbit, delta, L = 512, 0.14, 110
p, q, U, V, W = gen_rhyton(nbit, delta, L)

enc = encrypt(flag, p, q)

print(f'n = {p * q}')
print(f'V = {V}')
print(f'W = {W}')
print(f'enc = {enc}')