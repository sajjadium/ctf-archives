#!/bin/env sage
import json
import secrets
import sys
from pathlib import Path
from typing import List, Optional

from Crypto.Cipher import AES

def main(prog: Path, pubkey_path: Path, input_path: Path, output_path: Path) -> Optional[int]:
    # encrypt with AES GCM
    key = secrets.token_bytes(16)
    data = input_path.read_bytes()

    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    
    # load pk = (P, w)
    pubkey = json.loads(pubkey_path.read_bytes())
    P = matrix(GF(2), pubkey["P"])
    w = pubkey["w"]
    n = P.ncols()

    # convert input to message
    m = int.from_bytes(key)
    if not 0 <= m < binomial(n, w)-1:
        print(f"{prog}: input is too large", file=sys.stderr)
        return 2

    # encode message into error-space and encrypt
    e = vector(GF(2), encode(m, n, w))
    s = P * e

    # store output
    output_path.write_text(json.dumps({
        "ciphertext": {
            "data": ciphertext.hex(),
            "tag": tag.hex(),
            "nonce": cipher.nonce.hex(),
        },
        "s": list(map(int, s))
    }))

def encode(m: int, n: int, w: int) -> List[int]:
    assert 0 <= m < binomial(n, w)
    assert 0 <= w <= n
    e = []
    for n in range(n, 0, -1):
        bn = binomial(n - 1, w - 1)
        b = int(m < bn)
        e += [b]
        if b:
            w -= 1
        else:
            m -= bn
    return e

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(f"{sys.argv[0]}: missing arguments", file=sys.stderr)
    elif len(sys.argv) > 4:
        print(f"{sys.argv[0]}: too many arguments", file=sys.stderr)
    else:
        exit(main(Path(sys.argv[0]), Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])) or 0)
    print(f"Usage: {sys.argv[0]} PUBKEY IN OUT", file=sys.stderr)
    exit(1)

# vim: syntax=python
