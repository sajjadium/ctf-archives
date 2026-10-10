#!/usr/bin/env python3
"""
leaky-eval  --  an approximate-homomorphic evaluation service, bottled.

Ring-LWE in R_Q = Z_Q[X]/(X^N + 1), secret s with ternary coefficients.
A ciphertext of m is (a, b) with  b = a*s + e + m.

This is an APPROXIMATE scheme in the CKKS sense: decryption does not return m,
it returns m plus whatever noise is riding along. We publish, for each sample,
one single coefficient of that approximate decryption. One coefficient. The
noise is never published on its own and the key is never published at all.
"""
import json
from pathlib import Path
import secrets
from hashlib import sha256
from Crypto.Cipher import AES

N = 64
Q = (1 << 61) - 1                 # Mersenne prime 2^61 - 1
E_BOUND = 1 << 20                 # |noise coefficients|
NSAMPLES = 72                     # a little over N

def load_flag():
    """Author-side: the real flag lives in flag.txt, which is NOT distributed."""
    p = Path(__file__).with_name("flag.txt")
    return p.read_bytes().strip() if p.exists() else b"isfcr{REDACTED}"


FLAG = load_flag()


def negamul(f, g):
    """Multiply in Z_Q[X]/(X^N+1).  X^N = -1, so wrapped terms flip sign."""
    out = [0] * N
    for i, fi in enumerate(f):
        if not fi:
            continue
        for j, gj in enumerate(g):
            k = i + j
            if k < N:
                out[k] = (out[k] + fi * gj) % Q
            else:
                out[k - N] = (out[k - N] - fi * gj) % Q
    return out


def main():
    rng = secrets.SystemRandom()
    s = [rng.choice([-1, 0, 1]) for _ in range(N)]

    samples = []
    for _ in range(NSAMPLES):
        a = [rng.randrange(Q) for _ in range(N)]
        e = [rng.randrange(-E_BOUND, E_BOUND + 1) for _ in range(N)]
        a_s = negamul(a, s)
        # m = 0, so b = a*s + e
        b = [(a_s[i] + e[i]) % Q for i in range(N)]
        idx = rng.randrange(N)
        # the service discloses ONE coefficient of the approximate decryption
        # Dec(a,b) = b - a*s = e  (since m = 0)
        leak = e[idx] % Q
        samples.append({"a": a, "b": b, "idx": idx, "leak": leak})

    key = sha256((",".join(map(str, s))).encode()).digest()
    cipher = AES.new(key, AES.MODE_GCM, nonce=b"leaky-eval--")
    ct, tag = cipher.encrypt_and_digest(FLAG)

    json.dump({
        "N": N, "Q": Q, "E_BOUND": E_BOUND,
        "note": "secret s has coefficients in {-1,0,1}; every sample has m = 0",
        "samples": samples,
        "flag_ct": ct.hex(), "flag_tag": tag.hex(),
        "flag_nonce": b"leaky-eval--".hex(),
    }, open("output.json", "w"))
    print(f"[chall] wrote output.json  (N={N}, {NSAMPLES} samples)")


if __name__ == "__main__":
    main()
