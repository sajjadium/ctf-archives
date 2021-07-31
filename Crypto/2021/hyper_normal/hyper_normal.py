#!/usr/bin/env python3

import random
from flag import FLAG

p = 8443

def transpose(x):
	result = [[x[j][i] for j in range(len(x))] for i in range(len(x[0]))]
	return result

def vsum(u, v):
	assert len(u) == len(v)
	l, w = len(u), []
	for i in range(l):
		w += [(u[i] + v[i]) % p]
	return w

def sprod(a, u):
	w = []
	for i in range(len(u)):
		w += [a*u[i] % p]
	return w

def encrypt(msg):
	l = len(msg)
	hyper = [ord(m)*(i+1) for (m, i) in zip(list(msg), range(l))]
	V, W = [], []
	for i in range(l):
		v = [0]*i + [hyper[i]] + [0]*(l - i - 1)
		V.append(v)
	random.shuffle(V)
	for _ in range(l):
		R, v = [random.randint(0, 126) for _ in range(l)], [0]*l
		for j in range(l):
			v = vsum(v, sprod(R[j], V[j]))
		W.append(v)
	random.shuffle(transpose(W))
	return W

enc = encrypt(FLAG)
print(enc)