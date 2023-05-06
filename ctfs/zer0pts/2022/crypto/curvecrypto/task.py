import os
from random import randrange
from Crypto.Util.number import bytes_to_long, long_to_bytes, getStrongPrime
from Crypto.Util.Padding import pad
from fastecdsa.curve import Curve

def xgcd(a, b):
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0

def gen():
    while True:
        p = getStrongPrime(512)
        if p % 4 == 3:
            break
    while True:
        q = getStrongPrime(512)
        if q % 4 == 3:
            break
    n = p * q
    a = randrange(n)
    b = randrange(n)

    while True:
        x = randrange(n)
        y2 = (x**3 + a*x + b) % n
        assert y2 % n == (x**3 + a*x + b) % n
        if pow(y2, (p-1)//2, p) == 1 and pow(y2, (q-1)//2, q) == 1:
            yp, yq = pow(y2, (p + 1) // 4, p), pow(y2, (q + 1) // 4, q)
            _, s, t = xgcd(p, q)
            y = (s*p*yq + t*q*yp) % n
            break
    return Curve(None, n, a, b, None, x, y) 

def encrypt(m, G):
    blocks = [m[16*i:16*(i+1)] for i in range(len(m) // 16)]
    c = []
    for i in range(len(blocks)//2):
        G = G + G
        c.append(G.x ^ bytes_to_long(blocks[2*i]))
        c.append(G.y ^ bytes_to_long(blocks[2*i+1]))
    return c

def decrypt(c, G):
    m = b''
    for i in range(len(c) // 2):
        G = G + G
        m += long_to_bytes(G.x ^ c[2*i])
        m += long_to_bytes(G.y ^ c[2*i+1])
    return m

flag = pad(os.environ.get("FLAG", "fakeflag{sumomomomomomomomonouchi_sumomo_mo_momo_mo_momo_no_uchi}").encode(), 32)
C = gen()
c = encrypt(flag, C.G)
assert decrypt(c, C.G) == flag

print("n = {}".format(C.p))
print("a = {}".format(C.a))
print("b = {}".format(C.b))
print("c = {}".format(c))
