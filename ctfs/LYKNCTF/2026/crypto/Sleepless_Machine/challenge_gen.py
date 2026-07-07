import random

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import HKDF

from ntru_core import (
    generate_poly,
    invert_mod_q,
    poly_mul_cyclic,
    sum_even_odd,
    weighted_trace,
)

N = 127
Q = 4093
Q_PRIME = 1000003
P = 3
DENSITY = 0.36
TARGET_RANGE = 14

KDF_INFO = b"lyknctf-2026"


def _random_target(rng):
    return rng.randint(-TARGET_RANGE, TARGET_RANGE)


def _derive_key(s_alg, N_, q_, q_prime_):
    ikm = (
        s_alg.to_bytes(4, "big")
        + N_.to_bytes(2, "big")
        + q_.to_bytes(2, "big")
        + q_prime_.to_bytes(4, "big")
    )
    return HKDF(
        master=ikm,
        key_len=32,
        salt=str(N_).encode(),
        hashmod=SHA256,
        context=KDF_INFO,
    )


def generate_instance(flag: str, rng: random.Random) -> tuple[dict, dict]:
    se_f, so_f = _random_target(rng), _random_target(rng)
    se_g, so_g = _random_target(rng), _random_target(rng)

    f = generate_poly(N, Q, se_f, so_f, DENSITY, rng, need_invertible=True)
    g = generate_poly(N, Q, se_g, so_g, DENSITY, rng, need_invertible=False)

    f_inv = invert_mod_q(f, N, Q)
    h = poly_mul_cyclic(g, f_inv, N, Q)

    s_alg = weighted_trace(f, g, N, Q_PRIME)
    key = _derive_key(s_alg, N, Q, Q_PRIME)

    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(flag.encode())

    public_instance = {
        "ring": f"Z_{Q}[x]/(x^{N} - 1)",
        "parameters": {"N": N, "q": Q, "p": P, "q_prime": Q_PRIME},
        "public_key": {"h": h},
        "leakage": {
            "f_even_sum": se_f,
            "f_odd_sum": so_f,
            "g_even_sum": se_g,
            "g_odd_sum": so_g,
        },
        "encrypted_flag": {
            "nonce": cipher.nonce.hex(),
            "ciphertext": ciphertext.hex(),
            "tag": tag.hex(),
        },
    }
    secret = {"f": f, "g": g, "f_inv": f_inv, "s_alg": s_alg, "key": key}
    return public_instance, secret


def decrypt_with_secret(public_instance: dict, secret: dict) -> bytes:
    enc = public_instance["encrypted_flag"]
    cipher = AES.new(
        secret["key"],
        AES.MODE_GCM,
        nonce=bytes.fromhex(enc["nonce"]),
    )
    return cipher.decrypt_and_verify(
        bytes.fromhex(enc["ciphertext"]), bytes.fromhex(enc["tag"])
    )
