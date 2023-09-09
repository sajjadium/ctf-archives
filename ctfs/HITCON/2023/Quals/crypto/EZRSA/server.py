#!/usr/bin/env python3
from Crypto.Util.number import isPrime, getPrime, getRandomNBitInteger, getRandomRange
import gmpy2, os

# some generic elliptic curve stuff because sage is too heavy :(
# there is no intended vulnerability in part, please ignore it


class Curve:
    def __init__(self, p, a, b):
        self.p = gmpy2.mpz(p)
        self.a = gmpy2.mpz(a)
        self.b = gmpy2.mpz(b)

    def __eq__(self, other):
        if isinstance(other, Curve):
            return self.p == other.p and self.a == other.a and self.b == other.b
        return None

    def __str__(self):
        return "y^2 = x^3 + %dx + %d over F_%d" % (self.a, self.b, self.p)


class Point:
    def __init__(self, curve, x, y):
        if curve == None:
            self.curve = self.x = self.y = None
            return
        self.curve = curve
        self.x = gmpy2.mpz(x % curve.p)
        self.y = gmpy2.mpz(y % curve.p)
        lhs = (self.y * self.y) % curve.p
        rhs = (self.x * self.x * self.x + curve.a * self.x + curve.b) % curve.p
        if lhs != rhs:
            raise Exception("Point (%d, %d) is not on curve %s" % (x, y, curve))

    def __str__(self):
        if self == INFINITY:
            return "INF"
        return "(%d, %d)" % (self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.curve == other.curve and self.x == other.x and self.y == other.y
        return None

    def __add__(self, other):
        if not isinstance(other, Point):
            return None
        if other == INFINITY:
            return self
        if self == INFINITY:
            return other
        p = self.curve.p
        if self.x == other.x:
            if (self.y + other.y) % p == 0:
                return INFINITY
            else:
                return self.double()
        p = self.curve.p
        l = ((other.y - self.y) * gmpy2.invert(other.x - self.x, p)) % p
        x3 = (l * l - self.x - other.x) % p
        y3 = (l * (self.x - x3) - self.y) % p
        return Point(self.curve, x3, y3)

    def __neg__(self):
        return Point(self.curve, self.x, self.curve.p - self.y)

    def __mul__(self, e):
        if e == 0:
            return INFINITY
        if self == INFINITY:
            return INFINITY
        if e < 0:
            return (-self) * (-e)
        ret = INFINITY
        tmp = self
        while e:
            if e & 1:
                ret = ret + tmp
            tmp = tmp.double()
            e >>= 1
        return ret

    def __rmul__(self, other):
        return self * other

    def double(self):
        if self == INFINITY:
            return INFINITY
        p = self.curve.p
        a = self.curve.a
        l = ((3 * self.x * self.x + a) * gmpy2.invert(2 * self.y, p)) % p
        x3 = (l * l - 2 * self.x) % p
        y3 = (l * (self.x - x3) - self.y) % p
        return Point(self.curve, x3, y3)


INFINITY = Point(None, None, None)

# end of generic elliptic curve stuff


class ECRSA:
    # this is an implementation of https://eprint.iacr.org/2023/1299.pdf

    @staticmethod
    def gen_prime(sz):
        while True:
            u1 = getRandomNBitInteger(sz)
            u2 = getRandomNBitInteger(sz)
            up = 4 * u1 + 3
            vp = 4 * u2 + 2
            p = up**2 + vp**2
            if isPrime(p):
                return p, up, vp

    @staticmethod
    def generate(l):
        p, up, vp = ECRSA.gen_prime(l // 4)
        q, uq, vq = ECRSA.gen_prime(l // 4)
        n = p * q
        g = ((p + 1) ** 2 - 4 * up**2) * ((q + 1) ** 2 - 4 * uq**2)
        while True:
            e = getPrime(l // 8)
            if gmpy2.gcd(e, g) == 1:
                break
        priv = (p, up, vp, q, uq, vq)
        pub = (n, e)
        return ECRSA(pub, priv)

    def __init__(self, pub, priv=None):
        self.pub = pub
        self.n, self.e = pub
        self.priv = priv
        if priv is not None:
            self.p, self.up, self.vp, self.q, self.uq, self.vq = priv

    def compute_u(self, a, p, u, v):
        s = gmpy2.powmod(a, (p - 1) // 4, p)
        if s == 1:
            return -u
        elif s == p - 1:
            return u
        elif s * v % p == u:
            return v
        else:
            return -v

    def encrypt(self, m):
        r = getRandomRange(1, self.n)
        a = (m**2 - r**3) * gmpy2.invert(r, self.n) % self.n
        E = Curve(self.n, a, 0)
        M = Point(E, r, m)
        C = self.e * M
        return int(C.x), int(C.y)

    def decrypt(self, C):
        if self.priv is None:
            raise Exception("No private key")
        xc, yc = C
        a = (yc**2 - xc**3) * gmpy2.invert(xc, self.n) % self.n
        Up = self.compute_u(a, self.p, self.up, self.vp)
        Uq = self.compute_u(a, self.q, self.uq, self.vq)
        phi = (self.p + 1 - 2 * Up) * (self.q + 1 - 2 * Uq)
        d = gmpy2.invert(self.e, phi)
        E = Curve(self.n, a, 0)
        M = d * Point(E, xc, yc)
        return int(M.x), int(M.y)


def oracle_phase(ec: ECRSA):
    while True:
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Done")
        choice = int(input("> "))
        if choice == 1:
            m = int(input("m = "))
            print(ec.encrypt(m))
        elif choice == 2:
            C = tuple(map(int, input("C = ").split()))
            print(ec.decrypt(C))
        elif choice == 3:
            break


def challenge_phase(ec: ECRSA, n: int):
    for _ in range(n):
        m = getRandomRange(1, ec.n)
        C = ec.encrypt(m)
        print(f"{C = }")
        if int(input("m = ")) != m:
            return False
    return True


if __name__ == "__main__":
    flag = os.environ.get("FLAG", "flag{test_flag}")
    ec = ECRSA.generate(4096)
    oracle_phase(ec)
    if challenge_phase(ec, 16):
        print(flag)
