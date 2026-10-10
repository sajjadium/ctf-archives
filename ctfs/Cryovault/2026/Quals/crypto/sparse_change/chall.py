#!/usr/bin/env python3
"""
sparse-change  --  a decommissioned black box that evaluated a secret map.

The box held a secret polynomial over GF(p)

    F(X)  =  sum_{i=1..T}  c_i * X^(e_i)        (mod p)

with T = 24 terms, distinct exponents e_i < p-1 and nonzero coefficients.
Its degree is therefore up to p-2, about 2.3 * 10^18.

Before it was retired, the box was swept once: query j was the point g^j, for
j = 0, 1, ..., 2T-1, with g a generator of GF(p)*.  That log -- 48 outputs --
is all that survives.  The flag is sealed under F's term list.

Interpolating a degree-(p-2) polynomial needs p-1 evaluations and you have 48.
Guessing which of the p-1 possible exponents are the live ones is
C(p-1, 24) ~ 10^421 of them.  Neither of those is the intended route.
"""
import json
import secrets
from pathlib import Path
from hashlib import sha256

from sympy import isprime, primerange
from Crypto.Cipher import AES

PBITS = 61
T = 24                       # number of terms
NONCE = b"sparse-chnge"


def load_flag():
    """Author-side: the real flag lives in flag.txt, which is NOT distributed."""
    p = Path(__file__).with_name("flag.txt")
    return p.read_bytes().strip() if p.exists() else b"isfcr{REDACTED}"


FLAG = load_flag()


def gen_prime(rng):
    """A PBITS-bit prime p.  (p-1 is built from small factors, so that the
    exponents of F can be read back out of GF(p)* at all.)"""
    pool = list(primerange(1 << 14, 1 << 22))
    while True:
        prod, used = 2, []
        while prod.bit_length() < PBITS:
            q = rng.choice(pool)
            if q in used or (prod * q).bit_length() > PBITS:
                break
            prod *= q
            used.append(q)
        p = prod + 1
        if p.bit_length() == PBITS and isprime(p):
            return p, sorted(used) + [2]


def gen_generator(rng, p, facs):
    while True:
        g = rng.randrange(2, p - 1)
        if all(pow(g, (p - 1) // f, p) != 1 for f in facs):
            return g


def main():
    rng = secrets.SystemRandom()
    p, facs = gen_prime(rng)
    g = gen_generator(rng, p, facs)

    exps = rng.sample(range(1, p - 1), T)
    terms = sorted((e, rng.randrange(1, p)) for e in exps)

    def F(x):
        return sum(c * pow(x, e, p) for e, c in terms) % p

    log = [F(pow(g, j, p)) for j in range(2 * T)]

    key = sha256((";".join(f"{e}:{c}" for e, c in terms)).encode()).digest()
    cipher = AES.new(key, AES.MODE_GCM, nonce=NONCE)
    ct, tag = cipher.encrypt_and_digest(FLAG)

    json.dump({
        "p": p, "g": g, "t": T,
        "log": log,
        "note": "log[j] = F(g^j) for j = 0..2t-1;  F has exactly t terms, "
                "distinct exponents in [1, p-2], nonzero coefficients.  "
                "flag key = sha256 of ';'.join(f'{e}:{c}') over the terms "
                "sorted by exponent",
        "flag_ct": ct.hex(), "flag_tag": tag.hex(), "flag_nonce": NONCE.hex(),
    }, open(Path(__file__).with_name("output.json"), "w"))
    print(f"[chall] p = {p} ({p.bit_length()} bits), g = {g}")
    print(f"[chall] {T} terms, max exponent {max(e for e, _ in terms)}")
    print(f"[chall] published {2*T} evaluations")
    print("[chall] wrote output.json")


if __name__ == "__main__":
    main()
