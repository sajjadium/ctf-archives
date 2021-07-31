#!/usr/bin/env sage

from sage.all import *
from flag import flag

global p, alphabet
p = 71
alphabet = '=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ$!?_{}<>'

flag = flag.lstrip('CCTF{').rstrip('}')
assert len(flag) == 24

def cross(m):
	return alphabet.index(m)

def prepare(msg):
	A = zero_matrix(GF(p), 11, 11)
	for k in range(len(msg)):
		i, j = 5*k // 11, 5*k % 11
		A[i, j] = cross(msg[k])
	return A

def keygen():
	R = random_matrix(GF(p), 11, 11)
	while True:
		S = random_matrix(GF(p), 11, 11)
		if S.rank() == 11:
			_, L, U = S.LU()
			return R, L, U

def encrypt(A, key):
	R, L, U = key
	S = L * U
	X = A + R
	Y = S * X
	E = L.inverse() * Y
	return E

A = prepare(flag)
key = keygen()
R, L, U = key
S = L * U
E = encrypt(A, key)
print(f'E = \n{E}')
print(f'L * U * L = \n{L * U * L}')
print(f'L^(-1) * S^2 * L = \n{L.inverse() * S**2 * L}')
print(f'R^(-1) * S^8 = \n{R.inverse() * S**8}')