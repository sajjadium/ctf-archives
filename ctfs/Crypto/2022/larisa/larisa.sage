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

def pad(msg, n):
	assert len(msg) <= n
	return msg + msg[-1] * (n - len(msg))

def embed(msg, n):
	assert len(msg) < n
	msg = pad(msg, n)
	while True:
		r, s = [randint(2, n) for _ in '__']
		if gcd(r, len(msg)) == 1:
			break
	A = []
	for _ in range(n):
		while True:
			R = genperm(n)
			if R[(_ * r + s) % n] == ord(msg[_]):
				A.append(R)
				break
	return A

def encrypt(A, e = 65537):
	return powlat(A, e)

l, e = 128, 65537
M = embed(flag, l)
C = encrypt(M, e)
print(C)