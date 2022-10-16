#!/usr/bin/env python3

from Crypto.Util.number import *
from secret import params, flag

def keygen(nbit, k): # Pubkey function
	_p = 1
	while True:
		p, q = [_p + (getRandomNBitInteger(nbit - k) << k) for _ in '01']
		if isPrime(p) and isPrime(q):
			while True:
				s = getRandomRange(2, p * q)
				if pow(s, (p - 1) // 2, p) * pow(s, (q - 1) // 2, q) == (p - 1) * (q - 1):
					pubkey = p * q, s
					return pubkey

def encrypt(pubkey, m):
	n, s = pubkey
	r = getRandomRange(2, n)
	return pow(s, m, n) * pow(r, 2 ** k, n) % n

flag = flag.lstrip(b'ASIS{').rstrip(b'}')
nbit, k = params
PUBKEYS = [keygen(nbit, k) for _ in range(4)]
flag = [bytes_to_long(flag[i*8:i*8 + 8]) for i in range(4)]
ENCS = [encrypt(PUBKEYS[_], flag[_]) for _ in range(4)]

print(f'PUBKEYS = {PUBKEYS}')
print(f'ENCS = {ENCS}')