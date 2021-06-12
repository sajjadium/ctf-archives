import sys, json
from collections import namedtuple
from Crypto.Random.random import randrange

q = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
r = int(0x73eda753299d7d483339d80809a1d80553bda402fffe5bfeffffffff00000001)

F = GF(q, x, x)
F2.<x> = GF(q^2, x, x^2 + 1)

def down(t, x):
    return t(x.polynomial().mod(t.modulus()))

class Point(namedtuple("_Point", "x y")):
    def __init__(self, *args, **kw):
        assert self.is_valid()

    def is_valid(self):
        return self.is_inf() or self.x ^ 3 + down(self.x.parent(), 4*x + 4) == self.y ^ 2

    @property
    def inf(self):
        return type(self)(self.x.parent()(0), self.y.parent()(0))

    def is_inf(self):
        return self.x == self.y == 0

    def __add__(self, o):
        if self.is_inf():
            return o
        elif o.is_inf():
            return self
        if self != o and self.x == o.x:
            return self.inf
        if self == o:
            l = (3*(self.x^2))/(2*self.y)
        else:
            l = (self.y - o.y)/(self.x - o.x)
        nx = l^2 - self.x - o.x
        ny = l*(self.x - nx) - self.y
        return Point(nx, ny)

    def __neg__(self):
        return Point(self.x, -self.y)

    def __mul__(self, scalar):
        if scalar < 0:
            self = -self
            scalar = -scalar
        res = self.inf
        while scalar:
            if scalar & 1:
                res = res + self
            self = self + self
            scalar >>= 1
        return res

G1 = Point(F(4), F(0x0a989badd40d6212b33cffc3f3763e9bc760f988c9926b26da9dd85e928483446346b8ed00e1de5d5ea93e354abe706c)) * 0x396c8c005555e1568c00aaab0000aaab
G2 = Point(F2(2), F2(0x013a59858b6809fca4d9a3b6539246a70051a3c88899964a42bc9a69cf9acdd9dd387cfa9086b894185b9a46a402be73 + 0x02d27e0ec3356299a346a09ad7dc4ef68a483c3aed53f9139d2f929a3eecebf72082e5e58c6da24ee32e03040c406d4f*x)) * 0x5d543a95414e7f1091d50792876a202cd91de4547085abaa68a205b2e5a7ddfa628f1cb4d9e82ef21537e293a6691ae1616ec6e786f0c70cf1c38e31c7238e5

def format_v(v):
    return [hex(c) for c in v.polynomial().coefficients()]

def format_pt(P, name):
    return {f"{name}_x": format_v(P.x), f"{name}_y": format_v(P.y)}

def format_output(P_A, P_B, P_C):
    return {**format_pt(P_A, "P_A"), **format_pt(P_B, "P_B"), **format_pt(P_C, "P_C")}

def exchange_real():
    a = randrange(r)
    P_A = G1 * a
    b = randrange(r)
    P_B = G2 * b
    P_C = [P_B * a, P_A * b][randrange(int(2))]
    return format_output(P_A, P_B, P_C)

def exchange_fake():
    a = randrange(r)
    P_A = G1 * a
    b = randrange(r)
    P_B = G2 * b
    c = randrange(r)
    P_C = [G1, G2][randrange(int(2))] * c
    return format_output(P_A, P_B, P_C)

if __name__ == "__main__":
    with open(sys.argv[1], "rb") as f:
        flag = f.read()
    res = []
    for byte in flag:
        for bit in map(int, bin(byte)[2:].zfill(8)):
            if bit:
                res.append(exchange_real())
            else:
                res.append(exchange_fake())
    with open("out.txt", "w") as f:
        json.dump(res, f)
