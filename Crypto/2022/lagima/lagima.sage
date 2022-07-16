#!/usr/bin/env sage

from flag import flag

def genperm(n):
	_ = list(range(1, n + 1))
	shuffle(_)
	return _

def genlatrow(n):
	A = []
	for _ in range(n): A.append(genperm(n))
	return A

def prodlat(A, B):
	assert len(A) == len(B)
	C, G = [], SymmetricGroup(len(A))
	for _ in range(len(A)):
		g = (G(A[_]) * G(B[_])).tuple()
		C.append(list(g))
	return C

def powlat(A, n):
	assert n >= 0
	B = bin(n)[2:]
	c, R = len(B), [list(range(1, len(A) + 1)) for _ in range(len(A))]
	if n == 0: return R
	else:	
		for b in B:
			if b == '1':
				if c == 1: R = prodlat(R, A)
				else:
					T = A
					for _ in range(c - 1): T = prodlat(T, T)
					R = prodlat(R, T)
			c -= 1
	return R

G = genlatrow(313)
secret = int.from_bytes(flag.lstrip(b'CCTF{').rstrip(b'}'), 'big')
H = powlat(G, secret)

print(f'G = {G}')
print(f'H = {H}')
