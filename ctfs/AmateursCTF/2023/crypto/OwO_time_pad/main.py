import os
import random
from Crypto.Util.strxor import strxor
from math import gcd

with open('secret.txt', 'rb') as f:
    plaintext = f.read()
    keylength = len(plaintext)
    while gcd(keylength, len(plaintext)) > 1:
        keylength = random.randint(10, 100)
    key = os.urandom(keylength)
    key = key * len(plaintext)
    plaintext = plaintext * keylength
    ciphertext = strxor(plaintext, key)
    with open('out.txt', 'w') as g:
        g.write(ciphertext.hex())
