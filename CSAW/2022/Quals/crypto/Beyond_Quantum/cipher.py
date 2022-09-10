from cipher.mathutils import *
import numpy as np
from sympy.abc import x
from sympy.polys.polyerrors import NotInvertible
from sympy import ZZ, Poly
from collections import Counter


class Cipher:
    N = None
    p = None
    q = None
    f_poly = None
    g_poly = None
    h_poly = None
    f_p_poly = None
    f_q_poly = None
    R_poly = None

    def __init__(self, N, p, q):
        self.N = N
        self.p = p
        self.q = q
        self.R_poly = Poly(x ** N - 1, x).set_domain(ZZ)

    def generate_random_keys(self):
        g_poly = random_poly(self.N, int(math.sqrt(self.q)))
        tries = 10
        while tries > 0 and (self.h_poly is None):
            f_poly = random_poly(self.N, self.N // 3, neg_ones_diff=-1)
            try:
                self.generate_public_key(f_poly, g_poly)
            except NotInvertible as ex:
                tries -= 1
        if self.h_poly is None:
            raise Exception("Couldn't generate invertible f")

    def generate_public_key(self, f_poly, g_poly):
        self.f_poly = f_poly
        self.g_poly = g_poly
        self.f_p_poly = invert_poly(self.f_poly, self.R_poly, self.p)
        self.f_q_poly = invert_poly(self.f_poly, self.R_poly, self.q)
        p_f_q_poly = (self.p * self.f_q_poly).trunc(self.q)
        h_before_mod = (p_f_q_poly * self.g_poly).trunc(self.q)
        self.h_poly = (h_before_mod % self.R_poly).trunc(self.q)

    def encrypt(self, msg_poly, rand_poly):
        return (((self.h_poly).trunc(self.q) + msg_poly) % self.R_poly).trunc(self.q)

    def decrypt(self, msg_poly):
        a_poly = ((self.f_poly * msg_poly) % self.R_poly).trunc(self.q)
        b_poly = a_poly.trunc(self.p)
        return ((self.f_p_poly * b_poly) % self.R_poly).trunc(self.p)
