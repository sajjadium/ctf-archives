"""
As we known, LCG is NOT cryptographically secure.
So we designed these variants. Prove us wrong!
"""

from partial_challenge import gen_p1
from curve_challenge import gen_p2
from matrix_challenge import gen_p3
from secret import flag

from Crypto.Util.number import bytes_to_long, getStrongPrime
from os import urandom

p1 = gen_p1()
p2 = gen_p2()
p3 = gen_p3()
q = getStrongPrime(1024)
N = int(p1 * p2 * p3 * q)
flag = bytes_to_long(urandom(N.bit_length() // 8 - len(flag) - 1) + flag)
c = pow(flag, 0x10001, N)
print('N = {}'.format(hex(N)))
print('c = {}'.format(hex(c)))
