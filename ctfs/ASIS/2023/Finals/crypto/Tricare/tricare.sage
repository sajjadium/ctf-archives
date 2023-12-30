#!/usr/bin/env sage

from Crypto.Util.number import *
from secret import flag, seed

def encrypt(m, seed, precision):
	r = (20 * sin(m) ** 3 * cos(m) ** 3 - 6 * sin(m) * cos(m) * (sin(m) ** 4 + cos(m) ** 4)).n(precision)
	s = (1 - cos(6 * m) - seed * r).n(precision)
	t = (sin(6 * m) + seed * (cos(6 * m) + 1)).n(precision)
	u = (s / t).n(precision)
	return u

def shift(x, precision):
	u, v = (x**3 - 3*x).n(precision), (1 - 3*x**2).n(precision)
	w = (u / v).n(precision)
	return w

precision = 1363
m = bytes_to_long(flag)
t = encrypt(m, seed, precision)
s = shift(t, precision)

print(f's = {s}')