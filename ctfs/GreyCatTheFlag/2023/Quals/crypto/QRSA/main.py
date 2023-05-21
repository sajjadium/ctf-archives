from Crypto.Util.number import bytes_to_long
from secret import qa, qb, pa, pb

FLAG = b'fake_flag'

class Q:
    d = 41
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def __add__(self, other):
        return Q(self.a + other.a, self.b + other.b)
    
    def __sub__(self, other):
        return Q(self.a - other.a, self.b - other.b)
    
    def __mul__(self, other):
        a = self.a * other.a + Q.d * self.b * other.b
        b = self.b * other.a + self.a * other.b 
        return Q(a, b)

    def __mod__(self, other):
        # Implementation Hidden
        # ...
        return self
    
    def __str__(self) -> str:
        return f'({self.a}, {self.b})'
    
def power(a, b, m):
    res = Q(1, 0)
    while (b > 0):
        if (b & 1): res = (res * a) % m
        a = (a * a) % m
        b //= 2
    return res

p, q = Q(pa, pb), Q(qa, qb)
N = p * q
m = Q(bytes_to_long(FLAG[:len(FLAG)//2]), bytes_to_long(FLAG[len(FLAG)//2:]))
e = 0x10001
c = power(m, e, N)

print(f"N_a = {N.a}")
print(f"N_b = {N.b}")
print(f"C_a = {c.a}")
print(f"C_b = {c.b}")
print(f"e = {e}")
print(f"D = {Q.d}")