"""Prismwake's public observation and seal format.

The curve is E: Y^2 = X^3 + curve_b over F_p, where the decimal integers
prime and order in observations.json specify the field and subgroup order.
Each multiplier is reduced modulo order. The unpublished state consists of a
nonzero order-subgroup point K and one invertible
matrix (A, B; C, D), used for every observation:

    observation[i] = (A*x([multiplier[i]]K) + B)
                     / (C*x([multiplier[i]]K) + D)  (mod prime).

No point coordinates or matrix entries are included in the handout. The inverse
map has a unique representation x = (u*y + v)/(w*y + 1) for this instance.
Integers in the seal are encoded at the field's fixed byte width, big endian.
"""
import hashlib

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


def open_seal(data, x_of_k, u, v, w):
    p = int(data["prime"])
    width = (p.bit_length() + 7) // 8
    material = b"prismwake-v1\x00" + b"".join(
        (int(z) % p).to_bytes(width, "big") for z in (x_of_k, u, v, w)
    )
    key = hashlib.sha256(material).digest()
    return ChaCha20Poly1305(key).decrypt(
        bytes.fromhex(data["nonce"]), bytes.fromhex(data["ciphertext"]),
        b"prismwake-v1",
    )
