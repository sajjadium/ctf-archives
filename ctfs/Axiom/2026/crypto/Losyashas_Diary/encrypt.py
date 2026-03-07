#!/usr/bin/env python3
"""
Encryption scheme used in this challenge.
Key = SHA256(str(j_EA)), CTR mode with SHA256 as PRF.
"""

import hashlib


def encrypt(j_EA: int, plaintext: bytes) -> str:
    key = hashlib.sha256(str(j_EA).encode()).digest()
    ct = bytearray()
    for i in range((len(plaintext) + 31) // 32):
        block = hashlib.sha256(key + i.to_bytes(4, "big")).digest()
        for j in range(32):
            idx = i * 32 + j
            if idx < len(plaintext):
                ct.append(plaintext[idx] ^ block[j])
    return ct.hex()


def decrypt(j_EA: int, ct_hex: str) -> bytes:
    ct_bytes = bytes.fromhex(ct_hex)
    key = hashlib.sha256(str(j_EA).encode()).digest()
    pt = bytearray()
    for i in range((len(ct_bytes) + 31) // 32):
        block = hashlib.sha256(key + i.to_bytes(4, "big")).digest()
        for j in range(32):
            idx = i * 32 + j
            if idx < len(ct_bytes):
                pt.append(ct_bytes[idx] ^ block[j])
    return bytes(pt)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <j_EA> <ct_hex>")
        sys.exit(1)
    j = int(sys.argv[1])
    ct = sys.argv[2]
    print(decrypt(j, ct))
