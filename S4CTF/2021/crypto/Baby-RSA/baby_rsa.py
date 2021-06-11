#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Crypto.Util.number import *
from flag import flag

def create_tuple(nbit): # sorry for dirty code that is not performant!
	while True:
		p, q = [getPrime(nbit) for _ in range(2)]
		P = int(str(p) + str(q))
		Q = int(str(q) + str(p))
		if isPrime(P) and isPrime(Q):
			return P, Q

def encrypt(msg, pkey):
	return pow(bytes_to_long(msg), 31337, pkey)

nbit = 256
P, Q = create_tuple(nbit)
pkey = P * Q
enc = encrypt(flag.encode('utf-8'), pkey)

print('pkey =', pkey)
print('enc =', enc)