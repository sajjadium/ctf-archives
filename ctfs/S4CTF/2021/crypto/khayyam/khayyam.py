#!/usr/bin/env python3

from gmpy import *
from flag import FLAG

l = len(FLAG) // 2

x = int(FLAG[:l].encode("utf-8").hex(), 16)
y = int(FLAG[l:].encode("utf-8").hex(), 16)

p = next_prime(x)
q = next_prime(y)
e, n = 65537, p * q

m_1 = x + int(sqrt(y))
m_2 = y + int(sqrt(x))

c_1, c_2 = pow(m_1, e, n), pow(m_2, e, n)

print('A =', n**2 + c_1)
print('B =', c_2**2 - c_1**2)
print('C =', n**2 + c_2)