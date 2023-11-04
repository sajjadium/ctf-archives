# We don't think you need to worry too much about this file.

class EC:
    O = (0, 1, 0)

    def __init__(self, k, a):
        a1, a2, a3, a4, a6 = map(k, a)
        self.f = lambda x, y: y**2 + a1*x*y + a3*y - x**3 - a2*x**2 - a4*x - a6
        self.dfdx = lambda x, y: a1*y - 3*x**2 - 2*a2*x - a4
        self.dfdy = lambda x, y: 2*y + a1*x + a3
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.a4 = a4
        self.a6 = a6
        self.k = k

    def iszeropoint(self, p):
        if p == EC.O:
            return True
        x, y = p
        assert not (self.dfdx(x, y) == 0 and self.dfdy(x, y) == 0)
        return self.f(x, y) == self.k(0)

    def negate(self, p):
        if p == EC.O:
            return EC.O
        x, y = p
        return (x, -y - self.a1*x - self.a3)

    def add(self, p1, p2):
        assert (self.iszeropoint(p1) and self.iszeropoint(p2))
        if p1 == EC.O:
            return p2
        if p2 == EC.O:
            return p1
        if self.negate(p1) == p2:
            return EC.O
        if p1 == p2:
            x, y = p1
            x1, x2, y1, y2 = x, x, y, y
            l = (3*x**2 + 2*self.a2*x + self.a4 - self.a1*y) / \
                (2*y + self.a1*x + self.a3)
            n = (-x**3 + self.a4*x + 2*self.a6 - self.a3*y) / \
                (2*y + self.a1*x + self.a3)
        else:
            x1, y1 = p1
            x2, y2 = p2
            l = (y2 - y1) / (x2 - x1)
            n = (y1*x2 - y2*x1) / (x2 - x1)
        x3 = l**2 + self.a1*l - self.a2 - x1 - x2
        y3 = -(l + self.a1) * x3 - n - self.a3
        assert (self.iszeropoint((x3, y3)))
        return (x3, y3)

    def scalar(self, a, p):
        ret = EC.O
        i = 1
        tmp = p
        while i <= a:
            if (i & a) != 0:
                ret = self.add(ret, tmp)
            tmp = self.add(tmp, tmp)
            i <<= 1
        return ret
