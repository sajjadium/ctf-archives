#!/usr/bin/env python3

from Crypto.Util.number import *
import random


def genPrime():
    while True:
        a = random.getrandbits(256)
        b = random.getrandbits(256)

        if b % 3 == 0:
            continue

        p = a ** 2 + 3 * b ** 2
        if p.bit_length() == 512 and p % 3 == 1 and isPrime(p):
            return p


def add(P, Q, mod):
    m, n = P
    p, q = Q

    if p is None:
        return P
    if m is None:
        return Q

    if n is None and q is None:
        x = m * p % mod
        y = (m + p) % mod
        return (x, y)

    if n is None and q is not None:
        m, n, p, q = p, q, m, n

    if q is None:
        if (n + p) % mod != 0:
            x = (m * p + 2) * inverse(n + p, mod) % mod
            y = (m + n * p) * inverse(n + p, mod) % mod
            return (x, y)
        elif (m - n ** 2) % mod != 0:
            x = (m * p + 2) * inverse(m - n ** 2, mod) % mod
            return (x, None)
        else:
            return (None, None)
    else:
        if (m + p + n * q) % mod != 0:
            x = (m * p + (n + q) * 2) * inverse(m + p + n * q, mod) % mod
            y = (n * p + m * q + 2) * inverse(m + p + n * q, mod) % mod
            return (x, y)
        elif (n * p + m * q + 2) % mod != 0:
            x = (m * p + (n + q) * 2) * inverse(n * p + m * q + r, mod) % mod
            return (x, None)
        else:
            return (None, None)


def power(P, a, mod):
    res = (None, None)
    t = P
    while a > 0:
        if a % 2:
            res = add(res, t, mod)
        t = add(t, t, mod)
        a >>= 1
    return res


def random_pad(msg, ln):
    pad = bytes([random.getrandbits(8) for _ in range(ln - len(msg))])
    return msg + pad


p, q = genPrime(), genPrime()
N = p * q
phi = (p ** 2 + p + 1) * (q ** 2 + q + 1)

print(f"N: {N}")

d = getPrime(400)
e = inverse(d, phi)
k = (e * d - 1) // phi

print(f"e: {e}")

to_enc = input("> ").encode()
ln = len(to_enc)

print(f"Length: {ln}")

pt1, pt2 = random_pad(to_enc[: ln // 2], 127), random_pad(to_enc[ln // 2 :], 127)

M = (bytes_to_long(pt1), bytes_to_long(pt2))
E = power(M, e, N)

print(f"E: {E}")
