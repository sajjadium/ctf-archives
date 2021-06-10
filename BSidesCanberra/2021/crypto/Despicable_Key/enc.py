## ENCRYPT
## pip install pycryptodomex

from binascii import *
from Cryptodome.Cipher import AES

key = b'cybearscybears20'
import os
n = os.urandom(12)

with open('flag.png', 'rb') as f:
    d = f.read()

a = AES.new(key, AES.MODE_GCM, nonce=n)
cipher, tag = a.encrypt_and_digest(d)

with open('flag.png.enc', 'wb') as g:
    g.write(cipher)
