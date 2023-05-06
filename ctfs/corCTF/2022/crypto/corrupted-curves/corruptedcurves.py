#!/usr/local/bin/python
from secrets import randbits
from Crypto.Util.number import getPrime

def square_root(a, p):
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return 0
    elif p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    s = p - 1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1
    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e
    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)
        if m == 0:
            return x
        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m

def legendre_symbol(a, p):
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls

class EllipticCurve:
    
    def __init__(self, p, a, b):
        self.a = a
        self.b = b
        self.p = p
        if not self.check_curve():
            raise Exception("Not an elliptic curve!")
        
    def check_curve(self):
        discrim = -16 * (4*pow(self.a, 3) + 27*pow(self.b, 2))
        if discrim % self.p:
            return 1
        return 0
    
    def lift_x(self, px):
        y2 = (pow(px, 3) + self.a*px + self.b) % self.p
        py = square_root(y2, self.p)
        if py == 0:
            raise Exception("No point on elliptic curve.")
        return py

with open("flag.txt", "rb") as f:
    flag = f.read()
    flag = int.from_bytes(flag, 'big')

print("Generating parameters...")
while True:
    p = getPrime(512)
    a, b = randbits(384), randbits(384)
    try:
        E = EllipticCurve(p, a, b)
        fy = E.lift_x(flag)
        print(f"p = {p}")
        print(f"flag y = {fy}")
        break
    except:
        continue
checked = set()
count = 0
while count < 64:
    x = int(input("x = ")) % p
    if int(x) in checked or x < 2**384 or abs(x - p) < 2**384:
        print(">:(")
        continue
    e = randbits(64)
    print(f"e = {e}")
    try:
        E = EllipticCurve(p, a^e, b^e)
        py = E.lift_x(x)
        checked.add(int(x))
        print(f"y = {py}")
        count += 1
    except:
        print(":(")
print("bye!")