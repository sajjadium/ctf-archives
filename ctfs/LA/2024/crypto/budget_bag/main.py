import random
from hidden import DollarStore
p = 95773813056613526295315889615423014145567365190638271416026411091272805051097
def legendre(a, p):
    return pow(a, (p - 1) // 2, p)

def tonelli(n, p):
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        return pow(n, (p + 1) // 4, p)
    for z in range(2, p):
        if p - 1 == legendre(z, p):
            break
    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    t2 = 0
    while (t - 1) % p != 0:
        t2 = (t * t) % p
        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break
            t2 = (t2 * t2) % p
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r
class EllipticCurve:
    def __init__ (self, a, b, p):
        self.p = p
        self.a = a
        self.b = b
    def getPoint(self, x):
        ys = (x**3 + self.a*x + self.b) % p
        if legendre(ys, self.p) != 1:
            return None
        y = tonelli( ys ,p)
        return CurvePoint(x, y, self)
    
class CurvePoint:
    def __init__(self,x,y, curve):
        self.curve = curve
        self.x = x % curve.p
        self.y = y % curve.p
    def __str__(self):
        return f"({self.x},{self.y})"
    def __eq__(self, other):
        return str(self) == str(other)
    __repr__ = __str__
    def __add__(self, other):
        x1,y1 = self.x, self.y
        x2,y2 = other.x, other.y
        if x2 == 0 and y2 == 1:
            return self
        if x1 == 0 and y1 == 1:
            return other
        if x1 == x2 and y2 == self.curve.p - y1:
            return CurvePoint(0, 1, self.curve)
        if x1 == x2 and y1 == y2:
            lam = ((3*pow(x1, 2, self.curve.p) + self.curve.a) * pow(2* y1, -1, self.curve.p))% self.curve.p
        else:
            lam = ((y2 - y1) * pow(x2 - x1, -1, self.curve.p)) % self.curve.p
        x = (lam**2 - x1 - x2) % self.curve.p
        y = (lam*(x1 -x) - y1) % self.curve.p
        return CurvePoint(x, y, self.curve)


def scalar_mult(x, n, ec) -> CurvePoint:
    Q = x
    R = CurvePoint(0,1 ,ec)
    if n == 0: return R
    if n == 1: return x
    while n > 0:
        if n % 2 == 1:
            R = R + Q
        Q = Q + Q
        n = n // 2
    return R

flag = "lactf{REDACTED}" 

flag = flag.lstrip("lactf{").rstrip("}")

flagarray = [((random.randrange(2**10) >> 8) << 8) + ord(flag[i]) for i in range(len(flag))]

ec = DollarStore()

points = []
while len(points) < len(flagarray):
    x = random.randrange(p)
    point = ec.getPoint(x)
    if point != None:
        points.append(point)

s = scalar_mult(points[0], flagarray[0], ec)
for i in range(1,len(flagarray)):
    s += (scalar_mult(points[i], flagarray[i], ec))

print(f"s= {s}")

print(f"points = {points}")




