#!/usr/bin/env python3
"""
hidden-weights  --  the hidden subset sum problem.

I picked n secret weights a_1..a_n in Z_M, and for each of m rounds I picked a
secret subset of them and published only the sum:

        h_j  =  sum_i  a_i * x_{i,j}   mod M,      x_{i,j} in {0,1}

You get M, n, m and the h_j. You do not get the weights and you do not get the
subsets. Recover the weights.

(This is not ordinary subset-sum. In ordinary subset-sum the weights are
public and you hunt for the subset. Here BOTH are secret, which is why the
usual lattice does not apply.)
"""
import json
import secrets
from pathlib import Path
from hashlib import sha256
from Crypto.Cipher import AES
from sympy import nextprime

n, m = 10, 50
M = int(nextprime(1 << 200))
def load_flag():
    """Author-side: the real flag lives in flag.txt, which is NOT distributed."""
    p = Path(__file__).with_name("flag.txt")
    return p.read_bytes().strip() if p.exists() else b"isfcr{REDACTED}"


FLAG = load_flag()


def main():
    rng = secrets.SystemRandom()
    while True:
        alpha = [rng.randrange(M) for _ in range(n)]
        X = [[rng.randrange(2) for _ in range(m)] for _ in range(n)]
        h = [sum(alpha[i]*X[i][j] for i in range(n)) % M for j in range(m)]
        if pow(h[0], -1, M):           # need h_0 invertible for the lattice
            break

    key = sha256(",".join(map(str, sorted(alpha))).encode()).digest()
    c = AES.new(key, AES.MODE_GCM, nonce=b"hidden-wts--")
    ct, tag = c.encrypt_and_digest(FLAG)
    json.dump({"M": M, "n": n, "m": m, "h": h,
               "flag_ct": ct.hex(), "flag_tag": tag.hex(),
               "flag_nonce": b"hidden-wts--".hex(),
               "note": "key = SHA256(','.join(sorted(weights)))"},
              open("output.json", "w"), indent=1)
    print(f"[chall] n={n} m={m} log2(M)={M.bit_length()} -> output.json")

if __name__ == "__main__":
    main()
