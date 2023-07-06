#!/usr/bin/env python3
from Crypto.Util.number import getPrime
from random import randint

with open("/flag", "rb") as f:
    flag = int.from_bytes(f.read().strip(), "big")


def setup():
    # Get group prime + generator
    p = getPrime(512)
    g = 2

    return g, p


def key(g, p):
    # generate key info
    a = randint(2, p - 1)
    A = pow(g, a, p)

    return a, A


def encrypt_setup(p, g, A):
    def encrypt(m):
        k = randint(2, p - 1)
        c1 = pow(g, k, p)
        c2 = pow(A, k, p)
        c2 = (m * c2) % p

        return c1, c2

    return encrypt


def decrypt_setup(a, p):
    def decrypt(c1, c2):
        m = pow(c1, a, p)
        m = pow(m, -1, p)
        m = (c2 * m) % p

        return m

    return decrypt


def main():
    print("[$] Welcome to Morphing Time")

    g, p = 2, getPrime(512)
    a = randint(2, p - 1)
    A = pow(g, a, p)
    decrypt = decrypt_setup(a, p)
    encrypt = encrypt_setup(p, g, A)
    print("[$] Public:")
    print(f"[$]     {g = }")
    print(f"[$]     {p = }")
    print(f"[$]     {A = }")

    c1, c2 = encrypt(flag)
    print("[$] Eavesdropped Message:")
    print(f"[$]     {c1 = }")
    print(f"[$]     {c2 = }")

    print("[$] Give A Ciphertext (c1_, c2_) to the Oracle:")
    try:
        c1_ = input("[$]     c1_ = ")
        c1_ = int(c1_)
        assert 1 < c1_ < p - 1

        c2_ = input("[$]     c2_ = ")
        c2_ = int(c2_)
        assert 1 < c2_ < p - 1
    except:
        print("!! You've Lost Your Chance !!")
        exit(1)

    print("[$] Decryption of You-Know-What:")
    m = decrypt((c1 * c1_) % p, (c2 * c2_) % p)
    print(f"[$]     {m = }")

    # !! NOTE !!
    # Convert your final result to plaintext using
    # long_to_bytes

    exit(0)


if __name__ == "__main__":
    main()
