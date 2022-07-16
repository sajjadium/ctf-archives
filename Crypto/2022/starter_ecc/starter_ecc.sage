#!/usr/bin/env sage

from Crypto.Util.number import *
from secret import n, a, b, x, flag

y = bytes_to_long(flag.encode('utf-8'))

assert y < n
E = EllipticCurve(Zmod(n), [a, b])

try:
	G = E(x, y)
	print(f'x = {x}')
	print(f'a = {a}')
	print(f'b = {b}')
	print(f'n = {n}')
	print('Find the flag :P')
except:
	print('Ooops, ERROR :-(')