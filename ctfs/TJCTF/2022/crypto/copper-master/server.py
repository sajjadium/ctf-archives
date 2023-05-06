#!/usr/local/bin/python -u

from Crypto.Util.number import *
import os

N = 768
e = 3

p = 1
while GCD(e, p - 1) != 1:
    p = getPrime(N)

q = 1
while GCD(e, q - 1) != 1:
    q = getPrime(N)

n = p * q
d = pow(e, -1, (p - 1) * (q - 1))


def pad(m, n_bits):
    # otherwise recovering the message will be a bit of a pain...
    assert m.bit_length() <= 500

    return (0b111101010110111 << (n_bits - 15)) + \
           ((m ** 2) << 500) + \
           m

def unpad(m_padded):
    return m_padded & ((1 << 500) - 1)

def encrypt(m):
    m = pad(m, 1400)
    c = pow(m, e, n)
    return c

def decrypt(c):
    m = pow(c, d, n)
    m = unpad(m)
    return m

m = int.from_bytes(os.urandom(25), "big")
c = encrypt(m)
print(f"public key (n, e) = ({n}, {e})")
print(f"c = {c}")
guess = int(input("m = ? "))
if guess == m:
    print("Wow! How did you do that?")
    with open("flag.txt") as f:
        print(f.read())
else:
    print("Nice try, but I know my padding is secure!")
