
import os
import json
import random

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

rng = random.Random()
FLAG = os.getenv("FLAG").encode()

AMOUNT = 160

def generate_32bits():
    return b"".join(
        rng.getrandbits(32).to_bytes(4, "big")
        for _ in range(4)
    )

IVS = [generate_32bits() for _ in range(200)]
KEYS = [generate_32bits() + generate_32bits() for _ in range(200)] # RANDOM KEYS, should be EXTREMELY SECURE


def encrypt(plaintext, iv, key):
    cipher = AES.new(
        key,
        AES.MODE_CBC,
        iv
    )

    ciphertext = cipher.encrypt(
        pad(plaintext, 16)
    )

    return {
        "algorithm": "AES-256",
        "mode": "CBC",
        "iv": iv.hex(),
        "ciphertext": ciphertext.hex()
    }


with open("logs.jsonl","w") as f:
    for i in range(AMOUNT-1):
        plaintext = os.urandom(32)
        record = encrypt(plaintext, IVS[i], KEYS[i])

        record["record"] = i + 1
        f.write(json.dumps(record)+"\n")
    record = encrypt(FLAG, IVS[AMOUNT], KEYS[AMOUNT])
    record["record"] = AMOUNT
    f.write(json.dumps(record)+"\n")