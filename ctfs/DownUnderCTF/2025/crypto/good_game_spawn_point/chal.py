#!/usr/bin/env python3
import os
import secrets
import hashlib
from Crypto.Util.number import getPrime
from Crypto.PublicKey import ECC

FLAG = os.getenv("FLAG", "DUCTF{testflag}")

# https://neuromancer.sk/std/nist/P-256
order = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551 * 0x1


def ec_key():
    eck = ECC.generate(curve="p256")
    secret = int(eck.d)
    public_key = {
        "x": int(eck.public_key().pointQ.x),
        "y": int(eck.public_key().pointQ.y),
    }
    return secret, public_key


def paillier_key():
    p = getPrime(1024)
    q = getPrime(1024)
    n = p * q
    return p, q, n


def mta_response(ciphertext, n, secret):
    beta = secrets.randbelow(n)
    nsq = n * n

    # E(plaintext * secret)
    mta_response = pow(ciphertext, secret, nsq)

    # E(beta)
    r = secrets.randbelow(n)
    beta_enc = (pow(r, n, nsq) * pow(n + 1, beta, nsq)) % nsq

    # E(plaintext * secret + beta)
    mta_response = (mta_response * beta_enc) % nsq

    return mta_response, beta


def zk_schnorr(beta):
    r = secrets.randbelow(order)
    r_pub = ECC.construct(curve="p256", d=r % order).public_key().pointQ
    beta_pub = ECC.construct(curve="p256", d=beta % order).public_key().pointQ

    challenge_input = f"{beta}{order}{beta_pub}{r_pub}".encode()
    c_hash = int.from_bytes(hashlib.sha256(challenge_input).digest(), "big")
    z = (r + beta * c_hash) % order

    return {
        "hash": c_hash,
        "r_pub": {
            "x": int(r_pub.x),
            "y": int(r_pub.y),
        },
        "beta_pub": {
            "x": int(beta_pub.x),
            "y": int(beta_pub.y),
        },
    }


def main():
    print(
        """
        it's 4pm on a school afternoon. you just got home, tossed your bag
        on the floor, and turned on ABC3. it's time.. for GGSP
        """
    )

    secret, public_key = ec_key()
    print("public key:", public_key)

    p, q, n = paillier_key()
    print("paillier key:", {"p": p, "q": q})

    for _ in range(5):
        c = int(input("ciphertext:"))
        response, beta = mta_response(c, n, secret)
        print("mta response:", response)

        proof = zk_schnorr(beta)
        print("zk schnorr:", proof)

    guess = int(input("guess secret:"))
    if guess == secret:
        print("nice :o", FLAG)
    else:
        print("bad luck")


if __name__ == "__main__":
    main()
