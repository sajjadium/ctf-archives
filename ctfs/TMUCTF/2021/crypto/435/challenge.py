import binascii
import hashlib
import sys
from Crypto.Cipher import AES

key = b'*XhN2*8d%8Slp3*v'
key_len = len(key)


def pad(message):
    padding = bytes((key_len - len(message) % key_len) * chr(key_len - len(message) % key_len), encoding='utf-8')
    return message + padding


def encrypt(message, key, iv):
    aes = AES.new(key, AES.MODE_CBC, iv)
    return aes.encrypt(message)


h = hashlib.sha256(key).hexdigest()
hidden = binascii.unhexlify(h)[:10]
message = b'CBC (Cipher Blocker Chaining) is an advanced form of block cipher encryption' + hidden

with open('flag', 'rb') as f:
    IV = f.read().strip(b'TMUCTF{').strip(b'}')
    print(binascii.hexlify(encrypt(pad(message), key, IV)))
