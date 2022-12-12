"""
As we known, 
Linear means vulnerable.
So we put LCG on a curve to make it stronger.
"""
from sage.all import *
from Crypto.Util.number import getStrongPrime, getRandomRange


def gen_p2():
    p = getStrongPrime(1024)
    A = getRandomRange(p//2, p)
    B = getRandomRange(p//2, p)
    assert (4*A**3+27*B**2) % p != 0
    E = EllipticCurve(GF(p), [A, B])
    a = 1
    b = E.random_element()
    x = E.random_element()
    for i in range(7):
        x = a*x + b
        print('x{} = {}'.format(i, hex(x[0])))
    return p
