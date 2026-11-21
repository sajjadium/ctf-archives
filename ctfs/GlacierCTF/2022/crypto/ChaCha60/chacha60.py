#!/usr/bin/env python3
from Crypto.Cipher import ChaCha20
import numpy as np
import os
from binascii import hexlify

with np.load('matrices.npz') as f:
    m1 = f.get('m1')
    m2 = f.get('m2')
    m3 = f.get('m3')

if __name__ == '__main__':
    key = np.unpackbits(bytearray(os.urandom(8)), bitorder='little')
    k1 = m1.dot(key) % 2
    k2 = m2.dot(key) % 2
    k3 = m3.dot(key) % 2

    k1 = bytes(np.packbits(k1, bitorder='little'))
    k2 = bytes(np.packbits(k2, bitorder='little'))
    k3 = bytes(np.packbits(k3, bitorder='little'))

    print("base key: " + bytes(np.packbits(key, bitorder='little')).hex())
    print("exp. key: " + (k1 + k2 + k3).hex())

    k1 = k1 + b'\0' * 28
    k2 = k2 + b'\0' * 28
    k3 = k3 + b'\0' * 28

    nonce = b'\0' * 8
    c1 = ChaCha20.new(key=k1, nonce=nonce)
    c2 = ChaCha20.new(key=k2, nonce=nonce)
    c3 = ChaCha20.new(key=k3, nonce=nonce)

    with open('flag.png', 'rb') as f:
        pt = f.read()

    ct = c3.encrypt(c2.encrypt(c1.encrypt(pt)))

    with open('flag.png.enc', 'wb') as f:
        f.write(ct)
