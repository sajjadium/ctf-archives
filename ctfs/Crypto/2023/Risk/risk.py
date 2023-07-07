#!/usr/bin/env python3

from Crypto.Util.number import *
from secret import m, flag

def genPrime(m, nbit):
	assert m >= 2
	while True:
		a = getRandomNBitInteger(nbit // m)
		r = getRandomNBitInteger(m ** 2 - m + 2)
		p = a ** m + r
		if isPrime(p):
			return (p, r)

def genkey(m, nbit):
	p, r = genPrime(m, nbit // 2)
	q, s = genPrime(m, nbit // 2)
	n = p * q
	e = r * s
	return (e, n)

def encrypt(msg, pkey):
	e, n = pkey
	m = bytes_to_long(msg)
	c = pow(m, e, n)
	return c

pkey = genkey(m, 2048)
enc = encrypt(flag, pkey)

print(f'pkey = {pkey}')
print(f'enc = {enc}')