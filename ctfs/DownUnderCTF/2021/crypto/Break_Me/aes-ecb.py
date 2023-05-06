#!/usr/bin/python3
import sys
import os
from Crypto.Cipher import AES
from base64 import b64encode

bs = 16 # blocksize
flag = open('flag.txt', 'rb').read().strip()
key = open('key.txt', 'r').read().strip().encode() # my usual password

def enc(pt):
    cipher = AES.new(key, AES.MODE_ECB)
    ct = cipher.encrypt(pad(pt+key))
    res = b64encode(ct).decode('utf-8')
    return res

def pad(pt):
    while len(pt) % bs:
        pt += b'0'
    return (pt)

def main():
    print('AES-128')
    while(1):
        msg = input('Enter plaintext:\n').strip()
        pt = flag + str.encode(msg)
        ct = enc(pt)
        print(ct)

if __name__ == '__main__':
    main()
