import math
from sympy import GF, invert
import numpy as np
from sympy.abc import x
from sympy import ZZ, Poly


def is_prime(n):
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_2_power(n):
    return n != 0 and (n & (n - 1) == 0)

def random_poly(length, d, neg_ones_diff=0):
    result = Poly(np.random.permutation(
        np.concatenate((np.zeros(length - 2 * d - neg_ones_diff), np.ones(d), -np.ones(d + neg_ones_diff)))),
        x).set_domain(ZZ)
    return(result)

def invert_poly(f_poly, R_poly, p):
    inv_poly = None
    if is_prime(p):
        inv_poly = invert(f_poly, R_poly, domain=GF(p))
    elif is_2_power(p):
        inv_poly = invert(f_poly, R_poly, domain=GF(2))
        e = int(math.log(p, 2))
        for i in range(1, e):
            inv_poly = ((2 * inv_poly - f_poly * inv_poly ** 2) % R_poly).trunc(p)
    else:
        raise Exception("Cannot invert polynomial in Z_{}".format(p))
    return inv_poly
