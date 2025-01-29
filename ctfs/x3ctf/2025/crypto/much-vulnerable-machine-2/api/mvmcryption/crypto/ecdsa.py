"""Cryptography stuff."""

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from random import getrandbits
from secrets import randbelow

from Crypto.Util.number import bytes_to_long, long_to_bytes
from fastecdsa.curve import P256, Curve
from fastecdsa.ecdsa import verify
from fastecdsa.keys import get_public_key
from fastecdsa.point import Point

from mvmcryption.utils import decode, encode

CURVE = P256
N = CURVE.q


def private_key() -> int:
    f = Path("/etc/ecdsa-private-key")
    if not f.exists():
        privkey = randbelow(N)
        f.write_text(str(privkey))
    privkey = int(f.read_text())
    return privkey


def generate_nonce(k):
    """😇😇😇"""
    return getrandbits(k)


def encode_signature(signature: tuple[int, int]) -> str:
    """Encode signature to following format:
    `<r.b64>.<s.b64>`
    """
    r = encode(long_to_bytes(signature[0]))
    s = encode(long_to_bytes(signature[1]))

    return ".".join([r, s])


def decode_signature(encoded_signature: tuple[str, str]) -> tuple[int, int]:
    """Decode signature from the following format:
    `<r.b64>.<s.b64>`
    """
    r = bytes_to_long(decode(encoded_signature[0]))
    s = bytes_to_long(decode(encoded_signature[1]))

    return r, s


@dataclass
class ECDSA:
    private_key: int
    curve: Curve = P256

    def sign(self, msg: bytes) -> tuple[int, int]:
        z = int(sha256(msg).hexdigest(), 16) % N
        k = generate_nonce(128)  # 😇😇😇
        R = k * P256.G
        r = R.x % N
        s = (pow(k, -1, N) * (z + r * self.private_key)) % N
        return (r, s)

    @property
    def public_key(self) -> Point:
        return get_public_key(self.private_key, self.curve)

    def verify(self, signature: tuple[int, int], msg: bytes) -> bool:
        return verify(signature, msg, self.public_key, curve=self.curve)

    @property
    def pretty_public_key(self) -> dict:
        return {
            "curve": {
                "name": self.curve.name,
                "G": [hex(self.curve.gx), hex(self.curve.gy)],
                "p": hex(self.curve.p),
                "n": hex(self.curve.q),
            },
            "Q": [hex(self.public_key.x), hex(self.public_key.y)],
        }
