from secrets import randbelow
from hashlib import sha512

class Curve:
    def __init__(self, p, a, b) -> None:
        self.p = p
        self.a = a % p
        self.b = b % p
        self.O = Point(self, 0, 0)

class Point:
    def __init__(self, E: Curve, x: int, y: int) -> None:
        self.E = E
        self.x = x % E.p
        self.y = y % E.p

    def __neg__(self) -> 'Point':
        return Point(self.E, self.x, -self.y)

    def __add__(self, other: 'Point') -> 'Point':
        assert self.E == other.E
        E = self.E

        if other == E.O: return self
        if self  == E.O: return other

        xP, yP = self.x, self.y
        xQ, yQ = other.x, other.y

        if xP == xQ:
            if (yP + yQ) % E.p == 0:
                return E.O
            m = (3*xP**2 + E.a)*pow(2*yP, -1, E.p) % E.p
        else:
            m = (yQ - yP)*pow(xQ - xP, -1, E.p) % E.p

        xR = m**2 - xP - xQ
        yR = m*(xP - xR) - yP
        return Point(E, xR, yR)

    def __sub__(self, other: 'Point') -> 'Point':
        return self + -other

    def __mul__(self, k: int) -> 'Point':
        P, R = self, self.E.O
        if k < 0:
            P = -P
            k *= -1

        while k:
            if k % 2:
                R += P
            P += P
            k //= 2
        return R
    
    __rmul__ = __mul__

    def __eq__(self, o: 'Point') -> bool:
        return isinstance(o, Point) \
            and self.E == o.E       \
            and self.x == o.x       \
            and self.y == o.y

    def print(self, msg: str):
        print(msg)
        print('\tx =', self.x)
        print('\ty =', self.y)

    @staticmethod
    def input(msg: str):
        print(msg)
        x = int(input('\tx = '))
        y = int(input('\ty = '))
        return Point(E, x, y)

def H(P: Point) -> int:
    z = P.x.to_bytes(32, 'big') + P.y.to_bytes(32, 'big')
    return int.from_bytes(sha512(z).digest(), 'big') % p

def gen_key():
    a = randbelow(p)
    A = a*G
    return a, A

# The Sec in Secp256k1 is for Secure
p = 0xfffffffdffffffffffffffffffffffff
E = Curve(p, 0xfffffffdfffffffffffffffffffffffc, 0xe87579c11079f43dd824993c2cee5ed3)

Gx = 0x161ff7528b899b2d0c28607ca52c5b86
Gy = 0xcf5ac8395bafeb13c02da292dded7a83
G = Point(E, Gx, Gy)