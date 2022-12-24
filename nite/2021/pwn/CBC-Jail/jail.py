#!/usr/bin/python3 -u

import os, base64, sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

KEY=os.urandom(16)
IV=os.urandom(16)

def encrypt(msg):
    msg = pad(msg,16)
    cipher = AES.new(KEY,AES.MODE_CBC,IV)
    encrypted = cipher.encrypt(msg)
    encrypted = encrypted.hex()
    msg = IV.hex() + encrypted
    return msg

def decrypt(msg,iv):
    if len(msg) > 16:
        print("Message must be <= 16")
    cipher = AES.new(KEY,AES.MODE_CBC,iv)
    decrypted = unpad(cipher.decrypt(msg),16).decode()
    return decrypted

def weirdify(inp):
    iv = bytes.fromhex(inp[:32])
    msg = bytes.fromhex(inp[32:])
    command = decrypt(msg,iv)
    return command

banned = ['_', 'import','.','flag']

def crack():
  REDACTED

print('Welcome to Prison.')
print('A mad cryptographer thought it would be cool to mess your shell up.')
print('Lets see if you can "crack()" your way out of here')
print("As a gift we'll give you a sample encryption")
print(encrypt(b'trapped_forever'))

while True:
    try:
        inp = input(">>")
        inp = weirdify(inp)
        for w in banned:
            if w in inp:
                print("GOTTEM!!")
                sys.exit(0)
        exec(inp)
    except KeyboardInterrupt:
        print('\n')
        sys.exit(0)
