#!/usr/bin/env sage

from sage.all import *
from Crypto.Util.number import *
from secret import a, flag

def random_poly(degree):
	R.<x> = ZZ[]
	f = x**degree
	for i in range(1, degree):
		f += randint(-3, 3) * x ** (degree - i)
	return f

def genkey(a):
	M, N = [SL2Z.random_element() for _ in '01']

	A = N * matrix(ZZ, [[0, -1], [1, 1]]) * N**(-1)
	B = N * matrix(ZZ, [[0, -1], [1, 0]]) * N**(-1)
	r, s = [randint(5, 14) for _ in '01']
	U, V = (B * A) ** r, (B * A**2) ** s

	F = []
	for _ in range(2):
		Ux = [random_poly(randint(1, 4)) for _ in range(4)]
		Ux = [Ux[i] - Ux[i](a) + U[i // 2][i % 2] for i in range(4)]
		Ux = matrix([[Ux[0], Ux[1]], [Ux[2], Ux[3]]])
		F.append(Ux)

	X, Y = M * F[0] * M ** (-1), M * F[1] * M ** (-1)
	pubkey, privkey = (X, Y), (M, a)
	return pubkey, privkey

def encrypt(msg, pubkey):
	X, Y = pubkey
	C = Y
	for b in msg:
		C *= X ** (int(b) + 1) * Y
	return C

pubkey, privkey = genkey(a)
msg = bin(bytes_to_long(flag.lstrip(b'ASIS{').rstrip(b'}')))[2:]
enc = encrypt(msg, pubkey)

print(f'pubkey = {pubkey}')
print(f'enc = {enc}')