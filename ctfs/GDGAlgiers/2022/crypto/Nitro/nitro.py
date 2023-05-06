from sage.all import *

class Nitro:

    f_x = None
    g_x = None
    Fp_x = None
    Fq_x = None
    hx = None
    R = None
    Rq = None
    Rp = None

    def __init__(self, N, p, q, d):
        self.N = N
        self.p = p
        self.q = q
        self.d = d

    def random_poly(self, N, d1, d2):
        coef_list = [1] * d1 + [-1] * d2 + [0] * (N - d1 - d2)
        shuffle(coef_list)
        return  coef_list

    def keygen(self):
        RR= ZZ['x']
        Cyc = RR([-1]+[0]*(self.N - 1)+[1])#x^N-1
        R = RR.quotient(Cyc)
        Rq = RR.change_ring(Integers(self.q)).quotient(Cyc)
        Rp = RR.change_ring(Integers(self.p)).quotient(Cyc)
        while True:
            try:

                f_x = R(self.random_poly(self.N, self.d + 1, self.d))
                g_x = R(self.random_poly(self.N, self.d, self.d))
                Fp_x = Rp(lift(1 / Rp(f_x)))
                Fq_x = Rq(lift(1 / Rq(f_x)))
                break
            except:
                continue

        assert Fp_x * f_x == 1 and Fq_x * f_x == 1
        h_x = Rq(Fq_x * g_x)
        self.f_x, self.g_x, self.Fp_x, self.Fq_x, self.h_x = f_x, g_x, Fp_x, Fq_x, h_x
        self.R, self.Rq, self.Rp = R, Rq, Rp

    def encrypt(self, m: list):
        self.keygen()
        r_x = self.Rq(self.random_poly(self.N, self.d, self.d))
        m_x = self.Rp(m)
        m_x = m_x.lift()
        m_x = self.Rq(m_x)
        e_x = self.Rq(self.p * self.h_x * r_x + m_x)
        return e_x.list(), self.h_x.list()










