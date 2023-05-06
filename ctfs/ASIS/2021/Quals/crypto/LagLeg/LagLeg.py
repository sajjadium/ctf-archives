#!/usr/bin/env python3

from Crypto.Util.number import *
from gmpy import *
from math import gcd
from flag import flag

def lag(k, a, n):
	s, t = 2, a
	if k == 0:
		return 2
	r = 0
	while k % 2 == 0:
		r += 1
		k //= 2
	B = bin(k)[2:]
	for b in B:
		if b == '0':
			t = (s * t - a) % n
			s = (s **2 - 2) % n
		else:
			s = (s * t - a) % n
			t = (t** 2 - 2) % n
	for _ in range(r):
		s = (s ** 2 - 2) % n
	return s

def legkey(nbit):
	while True:
		r = getRandomNBitInteger(nbit >> 1)
		s = getRandomNBitInteger(nbit >> 3)
		p, q = r**5 + s, s + r
		if isPrime(p) and isPrime(q):
			while True:
				a = getRandomRange(2, q)
				if q*legendre(a, p) - p*legendre(a, q) == p - q:
					return p, q, a

def keygen(p, q, a):
	e = 65537
	if gcd(e, p**2 - 1) * gcd(e, q**2 - 1) < e:
		d = inverse(e, (p**2 - 1) * (q**2 - 1))
		x = pow(d, e, n)
		y = lag(x, a, p * q)
		return e, y, d

def encrypt(m, n, a, y, e):
	assert m < n
	r = getRandomRange(2, n)
	enc = (lag(r, a, n), (lag(r, y, n) + lag(e, m, n)) % n)
	return enc

p, q, a = legkey(512)
n = p * q
e, y, d = keygen(p, q, a)
m = bytes_to_long(flag)
c = encrypt(m, n, a, y, e)
print(f'a = {a}')
print(f'n = {n}')
print(f'y = {y}')
print(f'C = {c}')