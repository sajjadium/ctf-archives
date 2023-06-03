from sympy import GF
from hashlib import sha256
from dataclasses import dataclass
from hashlib import sha512


def H(message: str) -> bytes:
    return int.from_bytes(sha512(message.encode()).digest(), 'big') % q

# Ed448 curve
p = 2 ** 448 - 2 ** 224 - 1
# group order
q = 2 ** 446 - 0x8335dc163bb124b65129c96fde933d8d723a70aadc873d6d54a7bb0d

# field definition
GFp = GF(p)
GFq = GF(q)

# curve param
d = GFp(-39081)

# generator
B_x = GFp(224580040295924300187604334099896036246789641632564134246125461686950415467406032909029192869357953282578032075146446173674602635247710)
B_y = GFp(298819210078481492676017930443930673437544040154080242095928241372331506189835876003536878655418784733982303233503462500531545062832660)

def check_if_on_curve(x, y):
    a = 1
    return (a * x ** 2 + y ** 2) == (1 + d*x ** 2*y ** 2)

@dataclass
class Point():
    x:      int
    y:      int

    def _point_add(self, P, Q):
        # https://eprint.iacr.org/2008/522.pdf

        # check if both points are on the curve
        if not check_if_on_curve(P.x, P.y):
            raise Exception(f"Point {(P.x, P.y)} is not on the curve!")
        if not check_if_on_curve(Q.x, Q.y):
            raise Exception(f"Point {(Q.x, Q.y)} is not on the curve!")

        #if they are equal, double
        if (Q == P):
            return self._point_double(P)

        # projective coordinate Z = 1 for all points (coz we're working on affine :))
        A = GFp(1)
        B = A ** 2
        C = P.x * Q.x
        D = P.y * Q.y
        E = d * C * D
        F = B - E
        G = B + E

        H = (P.x + P.y) * (Q.x + Q.y)

        X = A * F * (H - C - D)
        Y = A * G * (D - C)
        Z = F * G

        # the result is in projective coords, switch to affine
        x = X / Z
        y = Y / Z

        return self.__class__(x, y)


    def _point_double(self, P):
        # https://eprint.iacr.org/2008/522.pdf

        # check if point is on the curve
        if not check_if_on_curve(P.x, P.y):
            raise Exception(f"Point {(P.x, P.y)} is not on the curve!")

        B = (P.x + P.y) ** 2
        C = P.x ** 2
        D = P.y ** 2
        E = C + D

        # projective coordinate Z = 1 for all points (coz we're working on affine :))
        H = GFp(1)
        J = E - 2 * H

        X = (B - E) * J
        Y = E * (C - D)
        Z = E * J

        # the result is in projective coords, switch to affine
        x = X / Z
        y = Y / Z

        return self.__class__(x, y)

    def _point_multiply(self, x, P):
        # check if point is on the curve
        if not check_if_on_curve(P.x, P.y):
            raise Exception(f"Point {(P.x, P.y)} is not on the curve!")

        Q = Point(GFp(0), GFp(1))  # Neutral element
        while x > 0:
            if x & 1:
                Q = Q + P
            P = P + P
            x >>= 1

        return Q

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __neg__(self):
        return self.__class__(self.x, -self.y)

    def __add__(self, other):
        return self._point_add(self, other)

    def __mul__(self, other: int):
        return self._point_multiply(other, self)

    def __rmul__(self, other: int):
        return self._point_multiply(other, self)

def check_if_on_twisted_curve(x, y):
    a = -1
    d_twisted = (d - 1)
    return (a * x ** 2 + y ** 2) == (1 + d_twisted * x ** 2 * y ** 2)

class EddysPoint(Point):
    # heh, I stole the idea to use isogeny from OpenSSL,
    # my implemention is so much better than Edd's. NO DOWNSIDES!!!
    # And he's supposed to be the smart guy, lol
    # https://eprint.iacr.org/2014/027.pdf

    def __init__(self, x, y, twist = True):
        if twist:
            self.x, self.y = self.isogeny(1, Point(x, y))
        else:
            self.x, self.y = (x, y)

    def untwisted(self):
        x, y = self.isogeny(-1, self)
        return (x, y)

    def isogeny(self, a, P):
        x = (2 * P.x * P.y) / (P.y ** 2 - a * P.x ** 2)
        y = (P.y ** 2 + a * P.x ** 2) / (2 - P.y ** 2 - a * P.x ** 2)
        return (x, y)

    def _point_add_twisted(self, P, Q):
        # https://eprint.iacr.org/2008/522.pdf
        # check if both points are on the curve
        if not check_if_on_twisted_curve(P.x, P.y):
            raise Exception(f"Point {(P.x, P.y)} is not on the curve!")
        if not check_if_on_twisted_curve(Q.x, Q.y):
            raise Exception(f"Point {(Q.x, Q.y)} is not on the curve!")

        #if they are equal, double
        if (Q == P):
            return self._point_double_twisted(P)

        Tp = P.x * P.y
        Tq = Q.x * Q.y

        # we can use a faster formula without d now!
        A = (P.y - P.x) * (Q.y + Q.x)
        B = (P.y + P.x) * (Q.y - Q.x)
        C = 2 * Tq
        D = 2 * Tp
        E = D + C
        F = B - A
        G = B + A
        H = D - C

        X = E * F
        Y = G * H
        Z = F * G

        # switch to affine
        x = X / Z
        y = Y / Z

        return self.__class__(x, y, False)

    def _point_double_twisted(self, P):
        # https://eprint.iacr.org/2008/522.pdf
        if not check_if_on_twisted_curve(P.x, P.y):
            raise Exception(f"Point {(P.x, P.y)} is not on the curve!")

        A = P.x ** 2
        B = P.y ** 2
        C = 2

        # twisted curve
        a = -1
        D = a * A
        E = (P.x + P.y) ** 2 - A - B
        G = D + B
        F = G - C
        H = D - B

        X = E * F
        Y = G * H
        Z = F * G

        # the result is in projective coords, switch to affine
        x = X / Z
        y = Y / Z

        return self.__class__(x, y, False)

    def _point_multiply_twisted(self, x, P):
        # check if point is on the curve
        if not check_if_on_twisted_curve(P.x, P.y):
            raise Exception(f"Point {(P.x, P.y)} is not on the curve!")

        Q = EddysPoint(GFp(0), GFp(1))  # Neutral element
        while x > 0:
            if x & 1:
                Q = self._point_add_twisted(P, Q)
            P = self._point_double_twisted(P)
            x >>= 1

        return Q

    def __add__(self, other):
        return self._point_add_twisted(self, other)

    def __mul__(self, other: int):
        return self._point_multiply_twisted(other, self)

    def __rmul__(self, other: int):
        return self._point_multiply_twisted(other, self)

if __name__ == "__main__":
    B = Point(B_x, B_y)

    assert not 3 * B == B + B, "Assertion error, (P * 3) = (P + P)"
    assert (B + (B)) + (B + B + B) == B * 5, "Assertion error, (P + P) + (P + P + P) != 5P"
    assert (B + B) + (B + B) == B * 2 + B * 2, "Assertion error, (P + P) + (P + P) != 2P + 2P"
    assert B * 2 + B * 3 == (B * 2) * 2 + B, "Assertion error, P*2 + P*3 != (P*2)*2 + 1"

    B = EddysPoint(B_x, B_y)

    assert not 3 * B == B + B, "Assertion error, (P * 3) = (P + P)"
    assert (B + (B)) + (B + B + B) == B * 5, "Assertion error, (P + P) + (P + P + P) != 5P"
    assert (B + B) + (B + B) == B * 2 + B * 2, "Assertion error, (P + P) + (P + P) != 2P + 2P"
    assert B * 2 + B * 3 == (B * 2) * 2 + B, "Assertion error, P*2 + P*3 != (P*2)*2 + 1"

    print("ok")