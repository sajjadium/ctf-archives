from .EllipticCurve import EllipticCurve
from .AffinePoint import AffinePoint

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


def jacobi_symbol(a, n):
    assert (n > a > 0 and n % 2 == 1)
    t = 1
    while a != 0:
        while a % 2 == 0:
            a /= 2
            r = n % 8
            if r == 3 or r == 5:
                t = -t
        a, n = n, a
        if a % 4 == n % 4 == 3:
            t = -t
        a %= n
    if n == 1:
        return t
    else:
        return 0


class WeierstrassCurve(EllipticCurve):

    def __init__(self, a, b, mod):
        self.a = a
        self.b = b
        self.mod = mod
        self.poif = AffinePoint(self, "infinity", "infinity")

    def is_singular(self):
        return (-16 * (4 * self.a ** 3 + 27 * self.b ** 2)) % self.mod == 0

    def _exp(self, base, e):
        return pow(base, e, self.mod)

    def calc_y_sq(self, x):
        return (self._exp(x, 3) + self.a * x + self.b) % self.mod

    def is_on_curve(self, point):
        return point is self.poif or self.calc_y_sq(point.x) == self._exp(point.y, 2)

    def enumerate_points(self):
        """
        Yields points of the curve.
        This only works well on tiny curves.
        """
        for i in range(self.mod):
            sq = self.calc_y_sq(i)
            y = self.sqrt(sq)

            if y:
                yield AffinePoint(self, i, y)
                yield AffinePoint(self, i, self.mod - y)

    def add(self, P, Q):
        """
         Sum of the points P and Q.
         Rules: https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication
        """
        if not (self.is_on_curve(P) and self.is_on_curve(Q)):
            raise ValueError(
                "Points not on basic_curves {}: {}, {}: {}".format(P, self.is_on_curve(P), Q, self.is_on_curve(Q)))

        # Cases with POIF
        if P == self.poif:
            result = Q
        elif Q == self.poif:
            result = P
        elif Q == self.invert(P):
            result = self.poif
        else:  # without POIF
            if P == Q:
                slope = (3 * P.x ** 2 + self.a) * self.inv_val(2 * P.y)
            else:
                slope = (Q.y - P.y) * self.inv_val(Q.x - P.x)
            x = (slope ** 2 - P.x - Q.x) % self.mod
            y = (slope * (P.x - x) - P.y) % self.mod
            result = AffinePoint(self, x, y)

        return result

    def __str__(self):
        return "y^2 = x^3 + {}x + {} mod {}".format(self.a, self.b, self.mod)
