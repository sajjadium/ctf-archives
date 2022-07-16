#!/usr/bin/env sage

from Crypto.Util.number import *
from secret import n, B, BASE_POINT, FLAG

m = bytes_to_long(FLAG)
assert m < n

F = IntegerModRing(n)
E = EllipticCurve(F, [31337, B])

BASE_POINT = E(BASE_POINT)

P = m * BASE_POINT
print(f'n = {n}')
print(f'BASE_POINT.x = {BASE_POINT.xy()[0]}')
print(f'P = {P.xy()[0], P.xy()[1]}')