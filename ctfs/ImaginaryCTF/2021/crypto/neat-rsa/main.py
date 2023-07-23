#!/usr/bin/python3

from Crypto.Util.number import getPrime, bytes_to_long
from os import urandom

with open('flag.txt', 'r') as f:
	flag = f.read()

p, q, r = [getPrime(512) for _ in range(3)]
n1, n2 = p * q, q * r

e = 65537

elusive = bytes_to_long(urandom(4))

pt = bytes_to_long(flag.encode())
ct = pow(pt, e, n1)

with open('rsa.txt', 'w') as g:
	g.write(f'n1 = {n1}\n')
	g.write(f'n2 + n1 * elusive = {n2 + n1 * elusive}\n')
	g.write(f'ct = {ct}\n')
