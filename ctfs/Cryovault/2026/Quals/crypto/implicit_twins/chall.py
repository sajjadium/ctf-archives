#!/usr/bin/env python3
"""
implicit-twins  --  two RSA keys that were generated carelessly.

Two independent 1275-bit moduli, N1 = p1*q1 and N2 = p2*q2. Different primes,
no common factor, nothing small, nothing close together. The flag is
RSA-encrypted under N1 with e = 65537.

The only thing wrong with them is something you cannot see: p1 and p2 came off
the same broken generator, so they agree on a long run of their low bits. How
long, I will not say.
"""
import json
import secrets
import math
from pathlib import Path
from hashlib import sha256
from sympy import isprime, nextprime

AQ, AP, T = 256, 1024, 530         # q bits, p bits, shared low bits of p (secret)
E = 65537
def load_flag():
    """Author-side: the real flag lives in flag.txt, which is NOT distributed."""
    p = Path(__file__).with_name("flag.txt")
    return p.read_bytes().strip() if p.exists() else b"isfcr{REDACTED}"


FLAG = load_flag()


def main():
    rng = secrets.SystemRandom()
    while True:
        low = rng.randrange(1 << T) | 1

        def make_p():
            while True:
                p = (rng.randrange(1 << (AP - T)) << T) | low
                if p.bit_length() == AP and isprime(p):
                    return p

        def make_q():
            return int(nextprime(rng.randrange(1 << (AQ - 1), 1 << AQ)))

        p1, p2 = make_p(), make_p()
        q1, q2 = make_q(), make_q()
        if len({p1, p2, q1, q2}) != 4:
            continue
        N1, N2 = p1 * q1, p2 * q2
        if math.gcd(N1, N2) != 1:
            continue
        if math.gcd(E, (p1 - 1) * (q1 - 1)) != 1:
            continue
        break

    m = int.from_bytes(FLAG, "big")
    assert m < N1
    ct = pow(m, E, N1)

    json.dump({"N1": N1, "N2": N2, "e": E, "ct": ct,
               "note": "flag = RSA-OAEP-free textbook encryption of the flag bytes under N1"},
              open("output.json", "w"), indent=1)
    print(f"[chall] N1 {N1.bit_length()}b  N2 {N2.bit_length()}b  "
          f"p {AP}b  q {AQ}b  shared-low-bits {T} (secret)")
    print(f"[chall] gcd(N1,N2) = {math.gcd(N1,N2)}")
    print("[chall] wrote output.json")


if __name__ == "__main__":
    main()
