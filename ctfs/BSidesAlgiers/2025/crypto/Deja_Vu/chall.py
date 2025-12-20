#!/usr/bin/env python3

import os
import json
import hashlib
import secrets
from dataclasses import dataclass

from Crypto.Util.number import long_to_bytes as lb
from Crypto.Cipher import AES

from secret import get_strong_prime, FLAG



def pkcs7_pad(data, block_size=16):
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len]) * pad_len


def sha256_key_from_secret(shared_secret, key_len=16):
    h = hashlib.sha256(lb(shared_secret)).digest()
    return h[:key_len]



@dataclass
class Party:
    name: str
    private_exponent: int

    def public_key(self, g, p):
        return pow(g, self.private_exponent, p)

    def shared_secret(self, other_public, p):
        return pow(other_public, self.private_exponent, p)


def load_log(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_log(path, records):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, sort_keys=False)


def append_record(path, record):
    records = load_log(path)
    records.append(record)
    save_log(path, records)


def encrypt_message_session(alice, bob, plaintext, bits_q=512, log_path="communications.json", isFlag=0):
    p = get_strong_prime(bits_q=bits_q)
    g = 2

    A = alice.public_key(g, p)
    B = bob.public_key(g, p)

    s_alice = alice.shared_secret(B, p)
    s_bob = bob.shared_secret(A, p)
    if s_alice != s_bob:
        raise RuntimeError("Shared secrets do not match")

    key = sha256_key_from_secret(s_alice, key_len=16)

    pt_bytes = plaintext
    padded = pkcs7_pad(pt_bytes, 16)
    ct = AES.new(key, AES.MODE_ECB).encrypt(padded)

    record = {
        "p": str(p),
        "g": str(g),
        "A": str(A),
        "B": str(B),
        "encrypted_hex": ct.hex(),
    }

    append_record(log_path, record)
    return record


def main():
    alice = Party("Alice", private_exponent=secrets.randbits(512))
    bob = Party("Bob", private_exponent=secrets.randbits(512))

    with open('messages.json','rb') as f:
        messages = json.load(f)

    for msg in messages:
        encrypt_message_session(alice, bob, msg.encode("utf-8"), bits_q=256, log_path="communications.json")

    encrypt_message_session(alice, bob, FLAG, bits_q=256, log_path="communications.json")
    
    


if __name__ == "__main__":
    main()
