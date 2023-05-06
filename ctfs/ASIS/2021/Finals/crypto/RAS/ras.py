#!/usr/bin/env python3

from Crypto.Util.number import *
from flag import flag

def genparam(nbit):
	while True:
		a, b = getRandomRange(2, nbit), getRandomRange(32, nbit)
		if (a ** b).bit_length() == nbit:
			return a ** b

def genkey(nbit):
	p, q = [_ + (_ % 2) for _ in [genparam(nbit) for _ in '01']]
	while True:
		P = p + getPrime(31)
		if isPrime(P):
			while True:
				Q = q + getPrime(37)
				if isPrime(Q):
					return P, Q

def encrypt(m, pubkey):
	e = 0x10001
	assert m < pubkey
	c = pow(m, e, pubkey)
	return c

nbit = 512
P, Q = genkey(nbit)
pubkey = P * Q
flag = bytes_to_long(flag)
enc = encrypt(flag, pubkey)
print(f'pubkey = {pubkey}')
print(f'enc = {enc}')