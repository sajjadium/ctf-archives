proof.all(False)

class EHasher:
    def __init__(self, p):
        self.p = p
        assert is_prime(self.p)

        self.A = GF(self.p)(612)
        self.B = GF(self.p)(721)
        self.E = EllipticCurve(GF(self.p), [0, self.A, 0, self.B, 0])

        self.Z = GF(self.p)(19)
        assert not is_square(self.Z)

    def helski(self, f):
        return f**((self.p - 1) / 2)

    def mafr(self, x):
        r = GF(self.p)(x).square_root()
        if ZZ(r) % 2 == 1:
            return -r
        return r

    def sioyek(self, r):
        w = -self.A / (1 + self.Z * r**2)
        e = self.helski(w**3 + self.A * w**2 + self.B * w)
        u = e * w - (1 - e) * (self.A / 2)
        v = -e * self.mafr(u**3 + self.A * u**2 + self.B * u)
        return self.E(u, v)

    def kuspel(self, r):
        assert 0 <= r < self.p
        return ZZ(self.sioyek(r)[0])

EHasherHellman = EHasher(2**80 - 65)
EHasherRemy = EHasher(2**80 - 143)
