#!/usr/bin/env sage

from Crypto.Util.number import *
from hashlib import sha512
from flag import flag

def genkey(nbit):
	while True:
		p = getPrime(nbit)
		if p % 4 == 3:
			q = int(str(p)[::-1])
			if isPrime(q):
				return p * q, (p, q)

def setup(msg, pkey):
	hid = sha512(msg).digest()
	while True:
		a = bytes_to_long(hid)
		if kronecker(a, pkey) == 1:
			return a
		else:
			hid = sha512(hid).digest()

def encrypt(msg, pkey):
	a, m = setup(msg, pkey), bytes_to_long(msg)
	B, C = bin(m)[2:], []
	for b in B:
		while True:
			t = randint(1, pkey)
			if kronecker(t, pkey) == 2 * int(b) - 1:
				C.append((t - a * inverse(t, pkey)) % pkey)
				break
	return (a, C)


pkey, privkey = genkey(512)
E = encrypt(flag, pkey)

print(f'pkey = {pkey}')
print(f'E = {E}')