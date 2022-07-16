#!/usr/bin/env python3

from Crypto.Util.number import *
from flag import flag

def keygen(nbit = 64):
	while True:
		k = getRandomNBitInteger(nbit)
		p = k**6 + 7*k**4 - 40*k**3 + 12*k**2 - 114*k + 31377
		q = k**5 - 8*k**4 + 19*k**3 - 313*k**2 - 14*k + 14011
		if isPrime(p) and isPrime(q):
			return p, q

def encrypt(msg, n, e = 31337):
	m = bytes_to_long(msg)
	return pow(m, e, n)

p, q = keygen()
n = p * q
enc = encrypt(flag, n)
print(f'n = {n}')
print(f'enc = {enc}')