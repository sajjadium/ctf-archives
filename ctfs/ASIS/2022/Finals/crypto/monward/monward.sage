#!/usr/bin/env sage

from Crypto.Util.number import *
from secret import C, flag

def monon(C, P):
	a, d, p = C
	x, y = P
	return (a*x**2 + y**2 - d*x**2*y**2) % p == 1

def monadd(C, P, Q):
	a, d, p = C
	assert monon(C, P) and monon(C, Q)
	x1, y1 = P
	x2, y2 = Q
	x3 = (x1 * y2 + y1 * x2) * inverse(1 + d * x1 * x2 * y1 * y2, p) % p
	y3 = (y1 * y2 - a * x1 * x2) * inverse(1 - d * x1 * x2 * y1 * y2, p) % p
	return (x3, y3)

def monprod(C, P, l):
	a, d, p = C
	x, y = P
	N, B = (0, 1), bin(l)[2:]
	for i in range(len(B)):
		if B[i] == '1':
			Q = P
			for _ in range(len(B) - i - 1):
				x, y = monadd(C, Q, Q)
				Q = (x, y)
			N = monadd(C, N, Q)
	return N

def encrypt(m, C, P):
	a, d, p = C
	assert m < p and monon(C, P)
	return monprod(C, P, m)

P = (2021000018575600424643989294466413996315226194251212294606, 1252223168782323840703798006644565470165108973306594946199)
Q = (2022000008169923562059731170137238192288468444410384190235, 1132012353436889700891301544422979366627128596617741786134)
R = (2023000000389145225443427604298467227780725746649575053047, 4350519698064997829892841104596372491728241673444201615238)

assert monon(C, P) == monon(C, Q) == monon(C, R) == is_prime(C[2]) == True
flag = flag.lstrip(b'ASIS{').rstrip(b'}')
m = bytes_to_long(flag)
enc = encrypt(m, C, P)
print(f'enc = {enc}')