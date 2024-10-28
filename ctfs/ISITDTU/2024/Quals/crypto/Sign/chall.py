#!/usr/bin/env python3

import os

from Crypto.Util.number import *
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256

flag = b'ISITDTU{aaaaaaaaaaaaaaaaaaaaaaaaaa}'
flag = os.urandom(255 - len(flag)) + flag


def genkey(e=11):
    while True:
        p = getPrime(1024)
        q = getPrime(1024)
        if GCD(p-1, e) == 1 and GCD(q-1, e) == 1:
            break
    n = p*q
    d = pow(e, -1, (p-1)*(q-1))
    return RSA.construct((n, e, d))


def gensig(key: RSA.RsaKey) -> bytes:
    m = os.urandom(256)
    h = SHA256.new(m)
    s = PKCS1_v1_5.new(key).sign(h)
    return s


def getflagsig(key: RSA.RsaKey) -> bytes:
    return long_to_bytes(pow(bytes_to_long(flag), key.d, key.n))


key = genkey()

while True:
    print(
        """=================
1. Generate random signature
2. Get flag signature
================="""
    )

    try:
        choice = int(input('> '))
        if choice == 1:
            sig = gensig(key)
            print('sig =', sig.hex())
        elif choice == 2:
            sig = getflagsig(key)
            print('sig =', sig.hex())
    except Exception as e:
        print('huh')
        exit(-1)
