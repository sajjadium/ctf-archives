from sage.all import *
from Crypto.Util.number import bytes_to_long
from secrets import SystemRandom
from secret import flag

class Point:
    def __init__(self, x, y) -> None:
        self.x = int(x)
        self.y = int(y)
    def __str__(self) -> str:
        return f"({self.x},{self.y})"

class Curve:
    def __init__(self) -> None:
        self.generate_parameters()

    def generate_parameters(self) -> None:
        rng = SystemRandom()

        self.p = random_prime(2**512-1, False, 2**511)
        self.k = rng.randint(1, self.p - 1)
        while True:
            x = rng.randint(1, self.p - 1)
            D = (self.k + (1 - self.k)*x**2) % self.p

            if legendre_symbol(D, self.p) == 1:
                r = rng.choice(GF(self.p)(D).nth_root(2, all=True))
                y = (1 + rng.choice([-1, 1])*r) * inverse_mod(x * (self.k - 1), self.p) % self.p
                self.G = Point(x, y)
                break
    
    def get_parameters(self):
        return self.G, self.k, self.p
    
    def add(self, P: Point, Q: Point) -> Point:
        x = ((1 + P.x*P.y + Q.x*Q.y)*inverse_mod(P.x*Q.x, self.p) + (1 + self.k)*P.y*Q.y) % self.p
        y = (P.y*(inverse_mod(Q.x, self.p) + Q.y) + (inverse_mod(P.x, self.p) + P.y)*Q.y) % self.p 
        # so weirddd :<
        return Point(inverse_mod(x - y, self.p), y)

    def mult(self, G: Point, k: int) -> Point:
        R = Point(1, 0)
        while k:
            if k&1:
                R = self.add(R, G)
            G = self.add(G, G)
            k >>= 1
        return R

curve = Curve()
G, k, p = curve.get_parameters()

print(f"G = {G}")
print(f"k = {k}")
print(f"p = {p}")
print(f"H = {curve.mult(G, bytes_to_long(flag))}")