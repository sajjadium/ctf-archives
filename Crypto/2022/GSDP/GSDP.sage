#!/usr/bin/env sage

from Crypto.Util.number import *
from flag import flag

def hash_base(m):
	m = M(m)
	_M = M(zero_matrix(d))
	for i in range(d):
		for j in range(d):
			_M[i, j] = pow(2, m[i, j], n)
	return M(_M)

def rand_poly(deg):
	P = PolynomialRing(Zn, 'x')
	x = P.gen()
	f = 0
	for _ in range(deg):
		f += randint(0, deg**2)*x**(_)
	return f

def matrox(a, b):
	a, b = M(a), M(b)
	R = zero_matrix(d)
	for i in range(d):
		for j in range(d):
			R[i, j] = int(a[i, j]) ^^ int(b[i, j])
	return M(R)

flag = flag.lstrip('CCTF{').rstrip('}')
assert len(flag) == 25
msg = [[ord(flag[j]) for j in range(5*i, 5*i + 5)] for i in range(5)]

nbit = 72
p, q = [getPrime(nbit) for _ in '01']
n = p * q

d, Zn = 5, Zmod(n)
M = MatrixSpace(Zn, d, d)

m = hash_base(msg)
u, v = [randint(2, 14) for _ in '01']
P = PolynomialRing(Zn, 'x')
x = P.gen()
f, h = rand_poly(d), x**d + x + 1
r, s = [random_matrix(Zn, d) for _ in '01']
y = f(r) ** u * s * f(r) ** v
c_1 = h(r) ** u * s * h(r) ** v
c_2 = matrox(hash_base(h(r) ** u * y * h(r) ** v), m)

print(f'n = {n}')
print(f'r = {r}')
print(f's = {s}')
print(f'y = {y}')
print(f'c_1 = {c_1}')
print(f'c_2 = {c_2}')