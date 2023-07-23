from Crypto.Util.number import *
from math import gcd


def keygen(sz):
    p = getPrime(sz // 2)
    q = getPrime(sz // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    e_fast = getPrime(sz // 2)
    # to make encryption more time consuming :P
    e_slow = e_fast + getPrime(sz // 3) * phi
    d = pow(e_fast, -1, phi)
    return (n, e_slow), (n, e_fast), (n, d)


def encrypt(pub, m):
    n, e = pub
    return pow(m, e, n)


def decrypt(priv, c):
    n, d = priv
    return pow(c, d, n)


pub, pub_fast, priv = keygen(2048)
m = bytes_to_long(open("flag.txt", "rb").read().strip())
c = encrypt(pub, m)
assert c == encrypt(pub_fast, m)
assert decrypt(priv, c) == m
print(f"{pub = }")
print(f"{c = }")
