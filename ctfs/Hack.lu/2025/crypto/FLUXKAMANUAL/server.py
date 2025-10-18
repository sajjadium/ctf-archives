#!/usr/bin/env nix-shell
#!nix-shell -i python -p python3Packages.pycryptodome
import os
import re
import secrets

from Crypto.Cipher import AES
from Crypto.Hash import SHA3_256
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

FLAG = os.environ.get("FLAG", "flag{FLUXKEA_USER_MANUAL}")
MASTERKEY = bytes.fromhex(os.environ.get("MASTERKEY", get_random_bytes(16).hex()))
SAMPLES = 7<<6

RE_CHALLENGE = re.compile("^[0-9a-fA-F]{1,32}$")

def expand(data: bytes) -> bytes:
    hasher = SHA3_256.new()
    hasher.update(data)
    output = hasher.digest()
    return output[16:], output[16:]

def encrypt(plaintext: bytes, key: bytes = None) -> bytes:
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(plaintext, AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return iv + ciphertext

def main():
    # encrypt user manual
    key = get_random_bytes(16)
    ciphertext = encrypt(FLAG.encode(), key)
    print("FluxKEA user manual:", ciphertext.hex())

    # interactive key transfer
    secret = int.from_bytes(key)
    tid = get_random_bytes(16)
    print("tansmission id:", tid.hex())
    key = MASTERKEY + tid
    for _ in range(SAMPLES):
        ikey, key = expand(key)
        otp = int.from_bytes(ikey)
        chal = input("challenge: ")
        assert RE_CHALLENGE.match(chal)
        chal = int(chal, 16)
        tk = ((secret + chal) * otp) % (1<<128)
        print("%32x" % tk)

if __name__ == "__main__":
    exit(main() or 0)
