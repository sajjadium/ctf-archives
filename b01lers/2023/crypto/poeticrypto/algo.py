#!/usr/bin/env python3

# Use these algorithms
from binascii import unhexlify, hexlify
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2

PUB_SALT = b'Grow grow grow!!'
PRIV_SALT_BITS = 16
KEY_SIZE = 32

from SECRET.keygen import getKey
from SECRET.vals import FLAG, SEED

class TreeOfLife:
    def __init__(self, seed, salt_len, key_len):
        self.seed = seed
        self.salt_len = salt_len
        self.key_len = key_len

    def burn(self, key):
        return AES.new(key, AES.MODE_GCM, nonce=b'00000000').encrypt(bytes(FLAG, 'ascii'))


if __name__ == "__main__":

    # Derive the key
    tree = TreeOfLife(SEED, PRIV_SALT_BITS, KEY_SIZE)
    key = getKey(tree, PUB_SALT)

    ct = tree.burn(key)
    print('CIPHERTEXT:', hexlify(ct).decode('ascii'))
