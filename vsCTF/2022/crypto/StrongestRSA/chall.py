from Crypto.Util.number import getStrongPrime, bytes_to_long
from sympy import prevprime, factorial
from math import gcd
import random

from secret import FLAG

e = 0x10001

def getStrongestPrime(nbits):
    while True:
        p = getStrongPrime(nbits)
        delta = random.randint(0x1337, 0x1337 + 0x1337)
        pp = p - delta
        ppp = prevprime(factorial(pp) % p)
        if gcd(ppp-1, e) == 1:
            return p, ppp
    
NBITS = 1024
p0, p = getStrongestPrime(NBITS)
q0, q = getStrongestPrime(NBITS)
N = p * q
m = bytes_to_long(FLAG.encode())
c = pow(m, e, N)

print(f"p0 = {p0}\nq0 = {q0}")
print(f"N = {N}\ne = {e}\nc = {c}")