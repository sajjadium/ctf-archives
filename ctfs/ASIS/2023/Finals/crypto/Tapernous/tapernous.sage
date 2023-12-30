#!/usr/bin/env sage

from secret import params, flag

def ginv(f, g):
	d, u, v = xgcd(f, g)
	return u.mod(g)

def ircp(t):
	while True:
		f = R.random_element(degree = t)
		if f.is_irreducible():
			g = R.random_element(degree = 13 + 37 * t)
			u = ginv(f, g)
			if u != 0:
				return f

def i2F(i, F):
	z, c = F.gen(), F.cardinality()
	l = log(c, 2)
	R.<z> = PolynomialRing(F)
	assert i < c
	coeffs = [int(_) for _ in list(bin(i)[2:].zfill(l))]
	poly = R(coeffs)
	return poly

def encode(msg, F, f):
	z, c = F.gen(), F.cardinality()
	l = F.cardinality()
	R = PolynomialRing(F, 'x')
	S = R.quotient(f, 'x')
	e, epoly = 0, S(0)
	for i in msg:
		epoly += i2F(i, F)(z) * S('x') ** e
		e += 1
	return epoly

def encrypt(msg, F, f):
	_enc = encode(msg, F, f)
	_r = randint(1, len(msg))
	for _ in range(_r):
		_enc = _enc ** 2
	return _enc

m, t = params
F = GF(2**m)
R = PolynomialRing(F, 'x')
f = ircp(t)
enc = encrypt(flag, F, f)

print(f'f = {f}')
print(f'c = {enc}')