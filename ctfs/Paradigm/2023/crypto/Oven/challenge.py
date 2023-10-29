#!/usr/bin/env python3
from Crypto.Util.number import *
import random
import os
import hashlib

FLAG = os.getenv("FLAG", "PCTF{flag}").encode("utf8")
FLAG = bytes_to_long(FLAG[5:-1])
assert FLAG.bit_length() < 384

BITS = 1024


def xor(a, b):
    return bytes([i ^ j for i, j in zip(a, b)])


# This doesn't really matter right???
def custom_hash(n):
    state = b"\x00" * 16
    for i in range(len(n) // 16):
        state = xor(state, n[i : i + 16])

    for _ in range(5):
        state = hashlib.md5(state).digest()
        state = hashlib.sha1(state).digest()
        state = hashlib.sha256(state).digest()
        state = hashlib.sha512(state).digest() + hashlib.sha256(state).digest()

    value = bytes_to_long(state)

    return value


def fiat_shamir():
    p = getPrime(BITS)
    g = 2
    y = pow(g, FLAG, p)

    v = random.randint(2, 2**512)

    t = pow(g, v, p)
    c = custom_hash(long_to_bytes(g) + long_to_bytes(y) + long_to_bytes(t))
    r = (v - c * FLAG) % (p - 1)

    assert t == (pow(g, r, p) * pow(y, c, p)) % p

    return (t, r), (p, g, y)


while True:
    resp = input("[1] Get a random signature\n[2] Exit\nChoice: ")
    if "1" in resp:
        print()
        (t, r), (p, g, y) = fiat_shamir()
        print(f"t = {t}\nr = {r}")
        print()
        print(f"p = {p}\ng = {g}\ny = {y}")
        print()
    elif "2" in resp:
        print("Bye!")
        exit()
