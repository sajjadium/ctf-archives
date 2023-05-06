#!/usr/bin/env python

import sys
import binascii
import base64
import string

if len(sys.argv) < 2:
    print "Usage: %s <plaintext message>" % sys.argv[0]
    sys.exit(1)

message = sys.argv[1]

def h(m):
    return binascii.hexlify(m)

def b(m):
    return base64.b64encode(m)

def r(m):
    t = string.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm")
    return string.translate(m,t)

def x(m):
    return ''.join(chr(ord(c)^0x42) for c in m)

def encrypt(s):
    print(b(x(h(r(s)))))

if __name__ == "__main__":
    encrypt(message)

