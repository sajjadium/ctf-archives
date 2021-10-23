#!/usr/bin/env sage

from sage.all import *
from Crypto.Util.number import *
from flag import flag

def rand_poly(n, N):
	R.<x> = PolynomialRing(Zmod(N))
	f = R(0)
	for i in range(n):
		f += randint(1, n-1) * x ** i
	return f

def keygen(nbit, l):
	p, q = [random_prime(2**nbit - 1) for _ in '01']
	e, N = randint(2, p * q - 1), p * q
	Zn = Zmod(N)
	f, A = rand_poly(l, N), random_matrix(Zn, l)
	B = f(A)
	phi = (p - 1) * (q - 1)
	d = inverse(e, phi)
	if e * d % N == 1:
		Q = B ** d
		pubkey = (e, N, Q, B)
		return pubkey

def encrypt(msg, pubkey):
	e, N, Q, B = pubkey
	l = Q.nrows()
	r = randint(2, N - 1)
	R, S = Q ** r, B ** r
	assert bytes_to_long(msg) < N
	c = pow(bytes_to_long(msg), e, N)
	C = [_ for _ in long_to_bytes(c)]
	CM = matrix(Zmod(N), [[pow(C[l*i + j], e, N) for j in range(l)] for i in range(l)])
	ENC = (CM * R, S)
	return ENC

nbit, l = 484, 11
pubkey = keygen(nbit, l)
ENC = encrypt(flag, pubkey)
print(f'pubkey = {pubkey}')
print(f'ENC = {ENC}')
