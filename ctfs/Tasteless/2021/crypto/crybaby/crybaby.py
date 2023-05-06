#!/usr/bin/env python3

import os
import sys
# pip install cryptography
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

key = os.urandom(16)

def from_user(msg):
    decryptor = Cipher(algorithms.AES(key), modes.CTR(nonce)).encryptor()
    return decryptor.update(msg) + decryptor.finalize()

def to_user(msg):
    encryptor = Cipher(algorithms.AES(key), modes.CTR(nonce)).encryptor()
    return (encryptor.update(msg) + encryptor.finalize())

# administrators must sign all their messages
def from_admin(msg):
    return AESGCM(key).decrypt(nonce, msg, associated_data=None)

def to_admin(msg):
    return AESGCM(key).encrypt(nonce, msg, associated_data=None)


print("cry baby cry")

admin = False
while True:
    nonce, msg = map(bytes.fromhex, sys.stdin.readline().split())

    if not admin:
        cmd = from_user(msg)
        if cmd == b'adminplz':
            admin = True
            print(to_user(b'Login successful!').hex())
        else:
            print(to_user(b'Unknown command!').hex())

    else:
        cmd = from_admin(msg)
        if cmd == b'flagplz':
            with open('flag', 'rb') as f:
                print(to_admin(f.read()).hex())
        else:
            print(to_admin(b'Unknown command!').hex())
