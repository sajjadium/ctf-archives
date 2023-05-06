"""
As we known, 
with some clever arithmetic, we can do fast skipping on LCG.
So we designed this challenge!
"""
from sage.all import *
from util import mt2dec


def gen_p3():
    n, m = 8, next_prime(2^16)
    A, B, X = [random_matrix(Zmod(m), n, n) for _ in range(3)]
    for i in range(1337**1337):
        if i < 10:
            print('X{} = {}'.format(i, hex(mt2dec(X, n, m))))
        X = A*X + B
    return next_prime(mt2dec(X, n, m))
