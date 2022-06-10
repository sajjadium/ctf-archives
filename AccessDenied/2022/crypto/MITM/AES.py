from Crypto.Cipher import AES
from binascii import hexlify, unhexlify
from hashlib import md5
import os
import signal


def get_ciphers(keys, iv1, iv2):
    return [ AES.new(keys[0], mode=AES.MODE_ECB), AES.new(keys[1], mode=AES.MODE_CBC, iv=iv1), AES.new(keys[2], mode=AES.MODE_CBC, iv=iv2) ]


def padding(m):
    return m + os.urandom(16 - (len(m) % 16))

def encrypt(m, keys, iv1, iv2):
    m = padding(m)
    ciphers = get_ciphers(keys, iv1, iv2)
    c = m
    for cipher in ciphers:
        c = cipher.encrypt(c)
    return c


def decrypt(c, keys, iv1, iv2):
    assert len(c) % 16 == 0
    ciphers = get_ciphers(keys, iv1, iv2)
    m = c
    for cipher in ciphers[::-1]:
        m = cipher.decrypt(m)
    return m