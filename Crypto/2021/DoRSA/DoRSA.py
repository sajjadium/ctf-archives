#!/usr/bin/env python3

from Crypto.Util.number import *
from math import gcd
from flag import FLAG

def keygen(nbit, dbit):
	assert 2*dbit < nbit
	while True:
		u, v = getRandomNBitInteger(dbit), getRandomNBitInteger(nbit // 2 - dbit)
		p = u * v + 1
		if isPrime(p):
			while True:
				x, y = getRandomNBitInteger(dbit), getRandomNBitInteger(nbit // 2 - dbit)
				q = u * y + 1
				r = x * y + 1
				if isPrime(q) and isPrime(r):
					while True:
						e = getRandomNBitInteger(dbit)
						if gcd(e, u * v * x * y) == 1:
							phi = (p - 1) * (r - 1)
							d = inverse(e, phi)
							k = (e * d - 1) // phi
							s = k * v + 1
							if isPrime(s):
								n_1, n_2 = p * r, q * s
								return (e, n_1, n_2)

def encrypt(msg, pubkey):
	e, n = pubkey
	return pow(msg, e, n)

nbit, dbit = 1024, 256

e, n_1, n_2 = keygen(nbit, dbit)

FLAG = int(FLAG.encode("utf-8").hex(), 16)

c_1 = encrypt(FLAG, (e, n_1))
c_2 = encrypt(FLAG, (e, n_2))

print('e =', e)
print('n_1 =', n_1)
print('n_2 =', n_2)

print('enc_1 =', c_1)
print('enc_2 =', c_2)

