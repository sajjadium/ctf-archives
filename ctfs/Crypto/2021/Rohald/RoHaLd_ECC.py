#!/usr/bin/env sage

from Crypto.Util.number import *
from secret import flag, Curve

def ison(C, P):
	c, d, p = C
	u, v = P
	return (u**2 + v**2 - c**2 * (1 + d * u**2*v**2)) % p == 0

def teal(C, P, Q):
	c, d, p = C
	u1, v1 = P
	u2, v2 = Q
	assert ison(C, P) and ison(C, Q)
	u3 = (u1 * v2 + v1 * u2) * inverse(c * (1 + d * u1 * u2 * v1 * v2), p) % p
	v3 = (v1 * v2 - u1 * u2) * inverse(c * (1 - d * u1 * u2 * v1 * v2), p) % p
	return (int(u3), int(v3))

def peam(C, P, m):
	assert ison(C, P)
	c, d, p = C
	B = bin(m)[2:]
	l = len(B)
	u, v = P
	PP = (-u, v)
	O = teal(C, P, PP)
	Q = O
	if m == 0:
		return O
	elif m == 1:
		return P
	else:
		for _ in range(l-1):
			P = teal(C, P, P)
		m = m - 2**(l-1)
		Q, P = P, (u, v)
		return teal(C, Q, peam(C, P, m))

c, d, p = Curve

flag = flag.lstrip(b'CCTF{').rstrip(b'}')
l = len(flag)
lflag, rflag = flag[:l // 2], flag[l // 2:]

s, t = bytes_to_long(lflag), bytes_to_long(rflag)
assert s < p and t < p

P = (398011447251267732058427934569710020713094, 548950454294712661054528329798266699762662)
Q = (139255151342889674616838168412769112246165, 649791718379009629228240558980851356197207)

print(f'ison(C, P) = {ison(Curve, P)}')
print(f'ison(C, Q) = {ison(Curve, Q)}')

print(f'P = {P}')
print(f'Q = {Q}')

print(f's * P = {peam(Curve, P, s)}')
print(f't * Q = {peam(Curve, Q, t)}')