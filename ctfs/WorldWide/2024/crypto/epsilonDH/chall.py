from Crypto.Util.number import getStrongPrime, getRandomNBitInteger, bytes_to_long
import os

p = getStrongPrime(1024)
flag = os.getenv("flag", "wwf{<REDACTED>}").encode()

class Epsilon:
    def __init__(self, a, b):
        self.a, self.b = a, b
    
    def __add__(self, other):
        if type(other) == int: other = Epsilon(other, 0)
        return Epsilon(self.a + other.a, self.b + other.b)
    def __radd__(self, other): return self.__add__(other)

    def __mul__(self, other):
        if type(other) == int: other = Epsilon(other, 0)
        return Epsilon(self.a * other.a, self.a * other.b + other.a * self.b)
    def __rmul__(self, other): return self.__mul__(other)

    def __mod__(self, other: int):
        return Epsilon(self.a % other, self.b % other)
    
    def __repr__(self): return f"{self.a} + {self.b}ɛ"

    @staticmethod
    def getRandomBits(n):
        return Epsilon(getRandomNBitInteger(n), getRandomNBitInteger(n))

def powm(b, e, m):
    r = 1
    while e > 1:
        if e & 1:
            r = (r * b) % m
        b = (b * b)  % m
        e >>= 1
    return (b * r) % m

ɛ = Epsilon(0, 1)
g = ɛ.getRandomBits(1024)
m = bytes_to_long(flag)
assert m < p
A = powm(g, m, p)

print(f"{p = }")
print(f"{g = }")
print(f"{A = }")
