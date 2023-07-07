#!/usr/bin/env python3

from Crypto.Util.number import *
from flag import flag

from decimal import *

def keygen(nbit, r):
	while True:
		p, q = [getPrime(nbit) for _ in '__']
		d, n = getPrime(64), p * q
		phi = (p - 1) * (q - 1)
		if GCD(d, phi) == 1:
			e = inverse(d, phi)
			N = bin(n)[2:-r]
			E = bin(e)[2:-r]
			PKEY = N + E
			pkey = (n, e)
			return PKEY, pkey

def encrypt(msg, pkey, r):
	m = bytes_to_long(msg)
	n, e = pkey
	c = pow(m, e, n)
	C = bin(c)[2:-r]
	return C

r, nbit = 8, 1024
PKEY, pkey = keygen(nbit, r)
print(f'PKEY = {int(PKEY, 2)}')
FLAG = flag.lstrip(b'CCTF{').rstrip(b'}')
enc = encrypt(FLAG, pkey, r)
print(f'enc = {int(enc, 2)}')