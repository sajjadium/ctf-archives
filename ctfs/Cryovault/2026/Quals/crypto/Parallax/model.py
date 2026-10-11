"""Parallax data model. The accompanying observations.json is the only instance.

All integer arithmetic in the observations is modulo ``prime`` unless stated.
The four hidden limbs are elements of [0, modulus). The public quadratic terms
are ordered by ``positions``. The public samples have the form

    sample[i] = sum(mask[i][j] * atom[j] for j in range(14)) % prime

for a hidden 40-by-14 binary mask. Its column weights are listed in the data.
Each atom is the evaluation below, perturbed by a nonzero centered integer
of magnitude at most ``error_limit``.

The payload has 28 ASCII bytes. Four consecutive seven-byte little-endian
chunks are transformed by the public odd multipliers and offsets modulo
``modulus``. These transformed limbs are the hidden values in the equations.
"""
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


def polynomial(data, j, limbs):
    p = int(data["prime"])
    v = int(data["constant"][j])
    v += sum(int(data["linear"][j][i]) * limbs[i] for i in range(4))
    v += sum(int(data["quad"][j][k]) * limbs[a] * limbs[b]
             for k, (a, b) in enumerate(data["positions"]))
    return v % p


def open_seal(data, limbs):
    encoded = b"".join(v.to_bytes(7, "little") for v in limbs)
    key = hashlib.sha256(b"parallax-v1\x00" + encoded).digest()
    return ChaCha20Poly1305(key).decrypt(
        bytes.fromhex(data["nonce"]), bytes.fromhex(data["ciphertext"]), b"parallax-v1"
    )
