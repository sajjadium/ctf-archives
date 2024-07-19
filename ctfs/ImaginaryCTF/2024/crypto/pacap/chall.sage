#!/usr/bin/env sage

from Crypto.Util.number import *
from flag import flag


def iscube(n, p):
    return pow(n, (p - 1) // gcd(3, p - 1), p) == 1


def issquare(n, p):
    return Mod(n, p).is_square()


def gen_prime(nbit, t):
    P = []
    for _ in range(t):
        while True:
            p = getPrime(nbit)
            if p % 3 * p % 4 == 3:
                P.append(p)
                break
    return P


def add(P, Q, c, n):
    # Add two points P and Q on curve x^3 + c*y^3 + c^2*z^3 - 3*c*x*y*z = 1 in Zmod(n)
    (x1, y1, z1) = P
    (x2, y2, z2) = Q
    x3 = (x1 * x2 + c * (y2 * z1 + y1 * z2)) % n
    y3 = (x2 * y1 + x1 * y2 + c * z1 * z2) % n
    z3 = (y1 * y2 + x2 * z1 + x1 * z2) % n
    return (x3, y3, z3)


def mul(P, g, c, n):
    # Scalar multiplication on curve
    (x1, y1, z1) = P
    (x2, y2, z2) = (1, 0, 0)
    for b in bin(g)[2:]:
        (x2, y2, z2) = add((x2, y2, z2), (x2, y2, z2), c, n)
        if b == "1":
            (x2, y2, z2) = add((x2, y2, z2), (x1, y1, z1), c, n)
    return (x2, y2, z2)


def keygen(nbit, r, s):
    p, q = gen_prime(nbit, 2)
    n, o = (
        p ^ r * q ^ s,
        p * q * (p ^ 2 + p + 1) * (q ^ 2 + q + 1) * (p - 1) ^ 2 * (q - 1) ^ 2,
    )
    e = randint(1, n)
    while gcd(e, o) != 1:
        e = randint(1, n)
    E = [
        p ^ (2 * (r - 1)) * q ^ (2 * (s - 1)) * (p ^ 2 + p + 1) * (q ^ 2 + q + 1),
        p ^ (2 * (r - 1)) * q ^ (2 * (s - 1)) * (p - 1) ^ 2 * (q - 1) ^ 2,
        p ^ (2 * (r - 1)) * q ^ (2 * (s - 1)) * (p ^ 2 + p + 1) * (q - 1) ^ 2,
        p ^ (2 * (r - 1)) * q ^ (2 * (s - 1)) * (p - 1) ^ 2 * (q ^ 2 + q + 1),
    ]
    D = [inverse(e, _) for _ in E]
    return (n, e), (p, q, D)


def encrypt(m, pubkey):
    (n, e) = pubkey
    (x, y) = m
    c = ((1 - x ^ 3) * inverse(y ^ 3, n)) % n
    enc = mul((x, y, 0), e, c, n)
    return enc


nbit, r, s = 1024, 4, 6
pubkey, _ = keygen(nbit, r, s)

l = len(flag)
m = (bytes_to_long(flag[: l // 2]), bytes_to_long(flag[l // 2 :]))
assert m[0] < pubkey[0] and m[1] < pubkey[0]
enc = encrypt(m, pubkey)

print(f"pubkey = {pubkey}")
print(f"enc = {enc}")
print(f"l = {l}")
