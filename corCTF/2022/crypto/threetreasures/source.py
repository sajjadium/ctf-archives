from sage.all import *
from Crypto.Util.number import bytes_to_long, getPrime
from random import getrandbits
from secret import flag, p, x, y

def random_pad(n, length):
    return (n << (length - n.bit_length())) + getrandbits(length - n.bit_length())

flag = bytes_to_long(flag)
fbits = flag.bit_length()
piece_bits = fbits // 3
a, b, c = flag >> (2 * piece_bits), (flag >> piece_bits) % 2**piece_bits, flag % 2**piece_bits
print(f'flag bits: {fbits}')
assert p.bit_length() == 512
q = getPrime(512)
n = p * q
ct = pow(random_pad(c, 512), 65537, n)
E = EllipticCurve(GF(p), [a, b])
G = E(x, y)
assert G * 3 == E(0, 1, 0)
print(f"n = {n}")
print(f"ct = {ct}")
print(f"G = {G}")
