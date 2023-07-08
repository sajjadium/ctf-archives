from CSR2023 import G
from hashlib import sha256
from random import SystemRandom

rng = SystemRandom()

len_mask = 2**(G.order.bit_length()+1)-1

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def inv(a, p):
    a %= p
    g, x, y = egcd(a, p)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % p


def check_bounds(v):
    if not (0 < v < G.order):
        raise ValueError(f"Invalid value not in bounds: {v}")


def create_sig(secret_key, msg):
    e = int.from_bytes(sha256(msg).digest(), "big")
    z = e & len_mask
    k = rng.randint(1, G.order - 1)
    P = k * G
    r = P.x 
    s = inv(k, G.order)  * (z  + r * secret_key) % G.order
    return r, s


def check_sig(pub_key, msg, sig):
    r, s = sig
    
    check_bounds(r)
    check_bounds(s)

    e = int.from_bytes(sha256(msg).digest(), "big")
    z = e & len_mask
    w = inv(s, G.order)
    u1 = z * w % G.order
    u2 = r * w % G.order
    P = u1 * G + u2 *pub_key
    return r == P.x


def generate_private_key():
    return rng.randint(1, G.order)


def generate_public_key(private_key):
    return private_key * G
    

