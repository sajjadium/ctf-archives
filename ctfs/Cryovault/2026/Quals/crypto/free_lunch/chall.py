#!/usr/bin/env python3
"""
free-lunch  --  a CICO problem on an arithmetization-oriented permutation.

The permutation P acts on GF(p)^2 for a prime p = 2 mod 3, in r rounds:

    (x, y)  <-  ( cbrt(x + y + c_i) ,  x )        i = 0 .. r-1

where cbrt(v) = v^(1/3) = v^e with 3e = 1 mod (p-1). Because p = 2 mod 3,
cubing is a bijection on GF(p), so the cube root is well defined and the
permutation is invertible. This is the shape used by arithmetization-oriented
designs: the round map is trivial to EVALUATE but its algebraic degree in the
forward direction is enormous.

    THE CHALLENGE (CICO -- constrained input, constrained output):
    find x such that P(x, 0) has its SECOND output coordinate equal to 0.

Public: p, r, the round constants. The flag is sealed under the smallest
such x.
"""
import json
import secrets
from pathlib import Path
from hashlib import sha256
from Crypto.Cipher import AES
from sympy import isprime
from flint import nmod_poly

R = 20
def load_flag():
    """Author-side: the real flag lives in flag.txt, which is NOT distributed."""
    p = Path(__file__).with_name("flag.txt")
    return p.read_bytes().strip() if p.exists() else b"isfcr{REDACTED}"


FLAG = load_flag()


def setup_prime():
    p = (1 << 62) - 57
    while not (isprime(p) and p % 3 == 2):
        p -= 1
    return p


def main():
    p = setup_prime()
    E = pow(3, -1, p - 1)
    cbrt = lambda v: pow(v % p, E, p)
    rng = secrets.SystemRandom()

    # --- plant one solution so the instance is guaranteed solvable ---
    while True:
        c = [rng.randrange(p) for _ in range(R)]
        x0 = rng.randrange(p)
        xs = {-1: 0, 0: x0}
        for i in range(0, R - 2):
            xs[i + 1] = cbrt(xs[i] + xs[i - 1] + c[i])
        c[R - 2] = (-(xs[R - 2] + xs[R - 3])) % p      # forces x_{R-1} = 0
        xs[R - 1] = cbrt(xs[R - 2] + xs[R - 3] + c[R - 2])
        if xs[R - 1] == 0:
            break

    def perm(x, y):
        for i in range(R):
            x, y = cbrt(x + y + c[i]), x
        return x, y
    assert perm(x0, 0)[1] == 0, "planted solution does not satisfy CICO"

    # --- the author runs the same attack, to learn ALL solutions ---
    P = {R: nmod_poly([0, 1], p), R - 1: nmod_poly([0], p)}
    for i in range(R - 1, -1, -1):
        P[i - 1] = P[i + 1] ** 3 - P[i] - nmod_poly([c[i] % p], p)
    F = P[-1]
    Xp = nmod_poly([0, 1], p)
    G = F.gcd(Xp.pow_mod(p, F) - Xp)
    sols = set()
    for root, _ in G.roots():
        t = int(root)
        a, b = t, 0                       # (x_r, x_{r-1})
        chain = {R: a, R - 1: b}
        for i in range(R - 1, -1, -1):
            chain[i - 1] = (pow(chain[i + 1], 3, p) - chain[i] - c[i]) % p
        if chain[-1] == 0 and perm(chain[0], 0)[1] == 0:
            sols.add(chain[0])
    assert x0 in sols, "planted solution not among recovered roots"
    answer = min(sols)

    key = sha256(str(answer).encode()).digest()
    ci = AES.new(key, AES.MODE_GCM, nonce=b"free-lunch--")
    ct, tag = ci.encrypt_and_digest(FLAG)
    json.dump({"p": p, "r": R, "c": c,
               "round": "(x,y) <- (cbrt(x+y+c_i), x);  cbrt(v)=v^(1/3) in GF(p)",
               "goal": "find x with P(x,0)[1] == 0",
               "note": "key = SHA256(decimal of the SMALLEST such x)",
               "flag_ct": ct.hex(), "flag_tag": tag.hex(),
               "flag_nonce": b"free-lunch--".hex()},
              open("output.json", "w"), indent=1)
    print(f"[chall] p={p} ({p.bit_length()} bits)  r={R}")
    print(f"[chall] deg F = {F.degree()};  {len(sols)} CICO solution(s)")
    print("[chall] wrote output.json")


if __name__ == "__main__":
    main()
