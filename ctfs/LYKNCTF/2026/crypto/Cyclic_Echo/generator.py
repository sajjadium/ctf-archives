import os
import random

from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from ntru import center, poly_inverse_cyclic, poly_mul_mod

N = 127
Q = 4093
Q_PRIME = 4099
LEAK_MOD = 127

DF_PLUS, DF_MINUS = 20, 19
DG_PLUS, DG_MINUS = 20, 20

KDF_INFO = b"lyknctf-2026"
MAX_KEYGEN_ATTEMPTS = 50


def _sample_ternary(n_plus, n_minus, n):
    idx = list(range(n))
    random.SystemRandom().shuffle(idx)
    poly = [0] * n
    for i in idx[:n_plus]:
        poly[i] = 1
    for i in idx[n_plus : n_plus + n_minus]:
        poly[i] = -1
    return poly


def _generate_keypair():
    f_inv = None
    f = None
    for _ in range(MAX_KEYGEN_ATTEMPTS):
        candidate = _sample_ternary(DF_PLUS, DF_MINUS, N)
        inv = poly_inverse_cyclic([c % Q for c in candidate], N, Q)
        if inv is not None:
            f, f_inv = candidate, inv
            break
    if f is None:
        raise RuntimeError("failed")

    g = _sample_ternary(DG_PLUS, DG_MINUS, N)
    h = poly_mul_mod([c % Q for c in g], f_inv, N, Q)

    assert center(poly_mul_mod([c % Q for c in f], h, N, Q), Q) == g

    return f, g, h


def _leak(poly):
    return {
        "even_sum_mod_P": sum(poly[0::2]) % LEAK_MOD,
        "odd_sum_mod_P": sum(poly[1::2]) % LEAK_MOD,
    }


def _algebraic_signature(f, g):
    return sum((i + 1) * f[i] * g[i] for i in range(N)) % Q_PRIME


def _derive_key(s_alg, salt):
    ikm = s_alg.to_bytes(2, "big") + N.to_bytes(2, "big") + Q.to_bytes(2, "big")
    return HKDF(master=ikm, key_len=32, salt=salt, hashmod=SHA256, context=KDF_INFO)


def generate_instance(flag: bytes):
    f, g, h = _generate_keypair()

    s_alg = _algebraic_signature(f, g)
    salt = os.urandom(16)
    key = _derive_key(s_alg, salt)

    nonce = os.urandom(12)
    aesgcm = AESGCM(key)
    ct_and_tag = aesgcm.encrypt(nonce, flag, None)
    ciphertext, tag = ct_and_tag[:-16], ct_and_tag[-16:]

    return {
        "parameters": {
            "N": N,
            "q": Q,
            "q_prime": Q_PRIME,
            "leak_modulus": LEAK_MOD,
            "ring": f"Z_{Q}[x]/(x^{N} - 1)",
            "df": {"plus": DF_PLUS, "minus": DF_MINUS},
            "dg": {"plus": DG_PLUS, "minus": DG_MINUS},
        },
        "public_key": {"h": h},
        "side_channel": {
            "f": _leak(f),
            "g": _leak(g),
        },
        "encrypted_flag": {
            "salt": salt.hex(),
            "nonce": nonce.hex(),
            "ciphertext": ciphertext.hex(),
            "tag": tag.hex(),
        },
    }
