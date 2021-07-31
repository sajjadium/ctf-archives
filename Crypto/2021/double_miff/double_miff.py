#!/usr/bin/env python3

from Crypto.Util.number import *
from secret import a, b, p, P, Q
from flag import flag

def onmiff(a, b, p, G):
	x, y = G
	return (a*x*(y**2 - 1) - b*y*(x**2 - 1)) % p == 0

def addmiff(X, Y):
	x_1, y_1 = X
	x_2, y_2 = Y
	x_3 = (x_1 + x_2) * (1 + y_1*y_2) * inverse((1 + x_1*x_2) * (1 - y_1*y_2), p) % p
	y_3 = (y_1 + y_2) * (1 + x_1*x_2) * inverse((1 + y_1*y_2) * (1 - x_1*x_2), p) % p
	return (x_3, y_3)


l = len(flag) // 2
m1, m2 = bytes_to_long(flag[:l]), bytes_to_long(flag[l:])

assert m1 < (p // 2) and m2 < (p // 2)
assert onmiff(a, b, p, P) and onmiff(a, b, p, Q)
assert P[0] == m1 and Q[0] == m2

print(f'P + Q = {addmiff(P, Q)}')
print(f'Q + Q = {addmiff(Q, Q)}')
print(f'P + P = {addmiff(P, P)}')



