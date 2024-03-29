#!/usr/bin/env sage

import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import sha256
import string
import random
import signal

assert("FLAG" in os.environ)
FLAG = os.environ["FLAG"]
assert(FLAG.startswith("openECSC{"))
assert(FLAG.endswith("}"))


def main():
    dim = 15
    k = 50
    n = 2**k
    Zn = Zmod(n)
    secret = ''.join(random.choice(string.ascii_letters) for _ in range(50))

    A = random_matrix(Zn, dim, dim-1) * random_matrix(Zn, dim-1, dim)

    print(f"A = {[row.list() for row in A]}")

    B = random_matrix(Zn, dim, dim-1) * random_matrix(Zn, dim-1, dim)

    print(f"B = {[row.list() for row in B]}")

    W = random_matrix(Zn, dim)

    print(f"W = {[row.list() for row in W]}")

    def random_pol(M, deg):
        res = 0
        for i in range(1, deg+1):
            res += Zn.random_element()*M**i
        return res

    L = random_pol(A, 20)
    M = random_pol(B, 20)

    U = L*W*M

    print(f"U = {[row.list() for row in U]}")

    R = random_pol(A, 20)
    S = random_pol(B, 20)

    V = R*W*S

    print(f"V = {[row.list() for row in V]}")

    key_a = L*V*M
    key_b = R*U*S
    assert key_a == key_b

    key = sha256(str(key_a).encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    enc_secret = cipher.encrypt(pad(secret.encode(), AES.block_size))

    print(f"enc_secret = {enc_secret.hex()}")

    guess = input("Can you retrieve the secret? ")
    if guess == secret:
        print(FLAG)
    else:
        print("Apparently no...")


def handler(signum, frame):
    print("Time over!")
    exit()


if __name__ == "__main__":
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(90)
    main()