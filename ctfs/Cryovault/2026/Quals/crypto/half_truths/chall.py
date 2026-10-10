#!/usr/bin/env python3
"""
half-truths  --  Shamir secret sharing, collected back from liars.

A degree-(K-1) polynomial f over GF(p) was sampled, and N shares (i, f(i))
handed out.  When the shares came back, only T of them were still honest; the
other N - T had been changed to something else.  Which ones, nobody wrote down.

The flag is sealed under the coefficients of f.

Reed-Solomon unique decoding -- Berlekamp-Welch, Gao, the extended Euclidean
key equation, every classical decoder -- corrects up to (N-K)/2 errors, i.e.
needs T >= (N+K)/2 honest shares.  Here T is well under that.  There is no
unique-decoding radius argument that reaches this instance, and that is not an
oversight.
"""
import json
import secrets
from pathlib import Path
from hashlib import sha256

from Crypto.Cipher import AES

P = (1 << 31) - 1          # Mersenne prime
K = 40                     # threshold: deg f = K-1 = 39
N = 512                    # shares handed out
T = 185                    # shares that came back honest
NONCE = b"half-truths-"


def load_flag():
    """Author-side: the real flag lives in flag.txt, which is NOT distributed."""
    p = Path(__file__).with_name("flag.txt")
    return p.read_bytes().strip() if p.exists() else b"isfcr{REDACTED}"


FLAG = load_flag()


def main():
    rng = secrets.SystemRandom()
    coeffs = [rng.randrange(P) for _ in range(K)]          # low -> high
    while coeffs[-1] == 0:
        coeffs[-1] = rng.randrange(P)

    def f(x):
        acc = 0
        for c in reversed(coeffs):
            acc = (acc * x + c) % P
        return acc

    xs = list(range(1, N + 1))
    honest = set(rng.sample(xs, T))
    shares = []
    for x in xs:
        if x in honest:
            shares.append([x, f(x)])
        else:
            y = rng.randrange(P)
            while y == f(x):                               # agreement is exactly T
                y = rng.randrange(P)
            shares.append([x, y])
    rng.shuffle(shares)

    key = sha256((",".join(map(str, coeffs))).encode()).digest()
    cipher = AES.new(key, AES.MODE_GCM, nonce=NONCE)
    ct, tag = cipher.encrypt_and_digest(FLAG)

    json.dump({
        "p": P, "k": K, "n": N, "t": T,
        "note": "shares are [x, y]; exactly t of them satisfy y = f(x), "
                "deg f = k-1; flag key = sha256 of f's coefficients, "
                "low-order first, decimal, comma-joined",
        "shares": shares,
        "flag_ct": ct.hex(), "flag_tag": tag.hex(), "flag_nonce": NONCE.hex(),
    }, open(Path(__file__).with_name("output.json"), "w"))
    print(f"[chall] p = 2^31-1, k = {K}, n = {N}, honest t = {T}")
    print(f"[chall] unique-decoding needs t >= (n+k)/2 = {(N+K)//2}; "
          f"errors here = {N-T} > (n-k)/2 = {(N-K)//2}")
    print("[chall] wrote output.json")


if __name__ == "__main__":
    main()
