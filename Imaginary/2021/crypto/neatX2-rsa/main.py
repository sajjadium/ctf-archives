#!/usr/bin/python3

from Crypto.Util.number import getPrime, bytes_to_long
from os import urandom

with open('flag.txt', 'r') as f:
	flag = f.read()

l = len(flag)
f1, f2 = flag[:l//2], flag[l//2:]

p, q, r = [getPrime(512) for _ in range(3)]
n1, n2 = p * q, q * r

e = 65537

elusive = bytes_to_long(urandom(4))

pt1 = bytes_to_long(f1.encode())
pt2 = bytes_to_long(f2.encode())

ct1 = pow(pt1, e, n1)
ct2 = pow(pt2, e, n2)

with open('rsa.txt', 'w') as g:
	g.write(f'n1 = {n1}\n')
	g.write(f'n2 + n1 * elusive = {n2 + n1 * elusive}\n')
	g.write(f'ct1 = {ct1}\n')
	g.write(f'ct2 = {ct2}\n')
