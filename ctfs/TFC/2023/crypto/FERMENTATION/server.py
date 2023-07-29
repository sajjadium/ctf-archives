#!/usr/bin/env python3
import pickle
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

KEY = os.urandom(16)
IV = os.urandom(16)
FLAG = 'redacted'

header = input("Header: ")
name = input("Name: ")
is_admin = False

data = header.encode() + pickle.dumps((name, is_admin))

encrypted = AES.new(KEY, AES.MODE_CBC, IV).encrypt(pad(data, 16))
print(encrypted.hex())

while True:
    data = bytes.fromhex(input().strip())
    try:
        if pickle.loads(unpad(AES.new(KEY, AES.MODE_CBC, IV).decrypt(data),16)[len(header):])[1] == 1:
            print(FLAG)
        else:
            print("Wait a minute, who are you?")
    except:
        print("Wait a minute, who are you?")