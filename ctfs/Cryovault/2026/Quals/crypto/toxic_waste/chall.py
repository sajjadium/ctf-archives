#!/usr/bin/env python3
"""
toxic-waste  --  a structured reference string that was compressed too far.

A trusted setup picked a secret tau and published the powers

    g, g^tau, g^(tau^2), ..., g^(tau^d)

in a prime-order subgroup G <= GF(P)*, then burned tau. Storing d+1 group
elements is expensive, so this deployment keeps only the two ends of the
chain: g^tau and g^(tau^d). Everything else was thrown away.

The claim on the tin is that recovering tau means solving a discrete log in
G, so the security is sqrt(q). Published here: P, q, g, d, g^tau, g^(tau^d).
The flag is sealed under tau.
"""
import json
import secrets
from pathlib import Path
from hashlib import sha256

from sympy import isprime
from Crypto.Cipher import AES

DBITS = 44                 # SRS degree d = 2^DBITS, a divisor of q-1
PBITS = 1024               # size of the ambient prime field
NONCE = b"toxic-waste-"


def load_flag():
    """Author-side: the real flag lives in flag.txt, which is NOT distributed."""
    p = Path(__file__).with_name("flag.txt")
    return p.read_bytes().strip() if p.exists() else b"isfcr{REDACTED}"


FLAG = load_flag()


def gen_subgroup_order(rng):
    """q prime, q - 1 = 2^DBITS * m with m prime.  So d = 2^DBITS divides q-1."""
    d = 1 << DBITS
    while True:
        m = rng.randrange(1 << (DBITS - 1), 1 << DBITS) | 1
        if not isprime(m):
            continue
        q = d * m + 1
        if isprime(q):
            return q, d, m


def gen_field(rng, q):
    """P prime with q | P - 1, and a generator g of the order-q subgroup."""
    while True:
        r = rng.randrange(1 << (PBITS - q.bit_length() - 2),
                          1 << (PBITS - q.bit_length() - 1))
        P = 2 * q * r + 1
        if P.bit_length() != PBITS or not isprime(P):
            continue
        cof = (P - 1) // q
        while True:
            h = rng.randrange(2, P - 1)
            g = pow(h, cof, P)
            if g != 1 and pow(g, q, P) == 1:
                return P, g


def main():
    rng = secrets.SystemRandom()
    q, d, m = gen_subgroup_order(rng)
    P, g = gen_field(rng, q)

    tau = rng.randrange(2, q - 1)
    A = pow(g, tau, P)                         # g^tau,      head of the SRS
    B = pow(g, pow(tau, d, q), P)              # g^(tau^d),  tail of the SRS

    key = sha256(str(tau).encode()).digest()
    cipher = AES.new(key, AES.MODE_GCM, nonce=NONCE)
    ct, tag = cipher.encrypt_and_digest(FLAG)

    json.dump({
        "P": P, "q": q, "g": g, "d": d,
        "A": A, "B": B,
        "note": "A = g^tau, B = g^(tau^d), both in the order-q subgroup of GF(P)*",
        "flag_ct": ct.hex(), "flag_tag": tag.hex(), "flag_nonce": NONCE.hex(),
    }, open(Path(__file__).with_name("output.json"), "w"))
    print(f"[chall] q is {q.bit_length()} bits, P is {P.bit_length()} bits, "
          f"d = 2^{DBITS}")
    print(f"[chall] (q-1)/d is {((q-1)//d).bit_length()} bits")
    print("[chall] wrote output.json")


if __name__ == "__main__":
    main()
