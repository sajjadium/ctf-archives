#!/usr/bin/env python3
from Crypto.Cipher import ARC4
import os
import gzip
import hashlib

SECRET = b"flag{REDACTED}"
assert len(SECRET) == 64

def compress(m):
    return gzip.compress(m)

def package(plaintext):
    KEY = os.urandom(32)
    plaintext = bytes.fromhex(plaintext)
    cipher = ARC4.new(KEY)
    enc = cipher.encrypt(compress(plaintext + SECRET))

    return enc.hex()

def banner():
    print('==============================================')
    print('You are connected to : Astynomoi Report Center')
    print('==============================================')

def main():
    banner()
    while True:
        try:
            print('How can I help you with?')
            print('1. Make report')
            print('2. Verify report')
            print('3. Exit')
            u = input('>> ')
            print('')
            if u == "1":
                print('Please type your report (in hex):')
                m = input(">> ")
                print(f"Here's your report: {package(m)}")
            elif u == "2":
                print("Please verify your signature before sending it.")
                print("Signature:", hashlib.sha256(SECRET).hexdigest())
            elif u == "3":
                print('See ya!')
                break
            print('')
        except:
            print('Error! Exiting...')
            break



if __name__ == '__main__':
    main()