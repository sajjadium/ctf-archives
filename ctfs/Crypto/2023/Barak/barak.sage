#!/usr/bin/env sage

from Crypto.Util.number import *
from flag import flag

def on_barak(P, E):
	c, d, p = E
	x, y = P
	return (x**3 + y**3 + c - d*x*y) % p == 0

def add_barak(P, Q, E):
	if P == (0, 0):
		return Q
	if Q == (0, 0):
		return P
	assert on_barak(P, E) and on_barak(Q, E)
	x1, y1 = P
	x2, y2 = Q
	if P == Q:
		x3 = y1 * (c - x1**3) * inverse(x1**3 - y1**3, p) % p
		y3 = x1 * (y1**3 - c) * inverse(x1**3 - y1**3, p) % p
	else:

		x3 = (y1**2*x2 - y2**2*x1) * inverse(x2*y2 - x1*y1, p) % p
		y3 = (x1**2*y2 - x2**2*y1) * inverse(x2*y2 - x1*y1, p) % p
	return (x3, y3)

def mul_barak(m, P, E):
	if P == (0, 0):
		return P
	R = (0, 0)
	while m != 0:
		if m & 1:
			R = add_barak(R, P, E)
		m = m >> 1
		if m != 0:
			P = add_barak(P, P, E)
	return R

def rand_barak(E):
	c, d, p = E
	while True:
		y = randint(1, p - 1)
		K = Zmod(p)
		P.<x> = PolynomialRing(K) 
		f = x**3 - d*x*y + c + y^3
		R = f.roots()
		try:
			r = R[0][0]
			return (r, y)
		except:
			continue

p = 73997272456239171124655017039956026551127725934222347
d = 68212800478915688445169020404812347140341674954375635
c = 1
E = (c, d, p)

P = rand_barak(E)

FLAG = flag.lstrip(b'CCTF{').rstrip(b'}')
m = bytes_to_long(FLAG) 
assert m < p
Q = mul_barak(m, P, E)
print(f'P = {P}')
print(f'Q = {Q}')