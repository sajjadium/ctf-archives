#!/usr/bin/env sage

from Crypto.Util.number import *
from flag import flag

def genkey(nbit, k):
	p = getPrime(nbit)
	q = getPrime(nbit >> 2)
	n = p * q
	N = (p**k - 1) * (q**k - 1)
	while True:
		e = getRandomRange(1, n)
		if gcd(e, n * N) == 1:
			pkey = e, n, N
			skey = p, q
			return (pkey, skey)

def two_layencrypt(msg, pkey):
	e, n, _ = pkey
	Zn = Zmod(n)
	m = bytes_to_long(msg)
	c = pow(m, e, n)
	_c = str(c)
	l = len(_c)
	_C = matrix(Zn, [[_c[:l//4], _c[l//4:l//2]], [_c[l//2:3*l//4], _c[3*l//4:l]]])
	assert gcd(det(_C), n) == 1
	C = _C ** e
	return C

k, nbit = 2, 1024

pkey, skey = genkey(nbit, k)
e, n, N = pkey

C = two_layencrypt(flag, pkey)

print(f'e = {e}')
print(f'n = {n}')
print(f'N = {N}')
print(f'C = {C}')