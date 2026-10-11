#!/usr/bin/env python3
"""Open the Monodromy v3 record after recovering the rotation index.

Requires `argon2-cffi` and `cryptography`. The work factor is fixed in the
public capsule. Incorrect work seeds still consume the full Argon2id work.
"""
import hashlib
import struct
import sys
from pathlib import Path

from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes


def parse(path):
    blob = Path(path).read_bytes()
    if len(blob) < 84 or blob[:8] != b"MONOVM3\0":
        raise ValueError("invalid Monodromy capsule")
    n0, n1 = struct.unpack_from("<II", blob, 32)
    memory_mib, iterations, lanes = struct.unpack_from("<III", blob, 56)
    seal_len = struct.unpack_from("<I", blob, 80)[0]
    tape_start = 84+seal_len
    if lanes != 1 or tape_start+(n0+n1)*19 != len(blob):
        raise ValueError("invalid capsule layout")
    artifact_hash = hashlib.sha256(blob[:80]+blob[tape_start:]).digest()
    return blob, artifact_hash, memory_mib, iterations, seal_len


def work_seed_from_index(index: int, path="capsule.bin") -> bytes:
    blob, artifact_hash, _, _, _ = parse(path)
    order = struct.unpack_from("<Q", blob, 24)[0]
    if not 0 <= index < order:
        raise ValueError("rotation index outside the public range")
    return hashlib.sha256(b"monodromy-v3-work\0"+index.to_bytes(8, "little")+
                          artifact_hash).digest()


def open_capsule(work_seed: bytes, path="capsule.bin") -> str:
    if len(work_seed) != 32:
        raise ValueError("work seed must be exactly 32 bytes")
    blob, artifact_hash, memory_mib, iterations, seal_len = parse(path)
    salt = hashlib.sha256(b"monodromy-v3-salt"+artifact_hash).digest()[:16]
    expensive = hash_secret_raw(secret=work_seed, salt=salt,
                                time_cost=iterations, memory_cost=memory_mib*1024,
                                parallelism=1, hash_len=32, type=Type.ID, version=19)
    key = HKDF(algorithm=hashes.SHA256(), length=32, salt=artifact_hash,
               info=b"monodromy-v3-flag").derive(expensive)
    return ChaCha20Poly1305(key).decrypt(blob[68:80], blob[84:84+seal_len],
                                         b"monodromy-v3"+artifact_hash).decode()


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        raise SystemExit("usage: python seal.py ROTATION_INDEX [capsule.bin]")
    path = sys.argv[2] if len(sys.argv) == 3 else "capsule.bin"
    print(open_capsule(work_seed_from_index(int(sys.argv[1]), path), path))
