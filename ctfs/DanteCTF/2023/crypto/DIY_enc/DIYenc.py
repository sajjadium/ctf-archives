#!/usr/bin/env python3

import os
from Crypto.Cipher import AES
from base64 import b64encode
from secret import FLAG

assert len(FLAG) == 19

if __name__ == '__main__':

    print('Encrypting flag...')
    key = os.urandom(16)
    nonce = os.urandom(15)
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    
    # longer ciphertext => safer ciphertext
    flag_enc = cipher.encrypt(FLAG*3).hex()
    print(f'Encrypted flag = {flag_enc}\n')

    print('You can choose only the length of the plaintext, but not the plaintext. You will not trick me :)')
    for i in range(7):
        length = int(input('> '))
        assert length > 3 and length < 100, "Invalid input"
        pt = b64encode(os.urandom(length))
        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
        ct = cipher.encrypt(pt).hex()
        print(f'ct = {ct}')
    print('Enough.')
