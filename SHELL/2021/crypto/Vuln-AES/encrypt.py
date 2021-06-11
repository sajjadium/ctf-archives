#!/usr/bin/env python3

import base64
from Crypto.Cipher import AES

secret_code = "<flag>"

def pad(message):
    if len(message) % 16 != 0:
        message = message + '0'*(16 - len(message)%16 )    #block-size = 16
    return message

def encrypt(key, plain):
    cipher = AES.new( key, AES.MODE_ECB )
    return cipher.encrypt(plain)

sitrep = str(input("Crewmate! enter your situation report: "))
message = '''sixteen byte AES{sitrep}{secret_code}'''.format(sitrep = sitrep, secret_code = secret_code) #the message is like [16-bytes]/[report]/[flag]

message = pad(message)
message1 = bytes(message,'utf-8')

cipher = encrypt( b'sixteen byte key', message1 )
cipher = base64.b64encode(cipher)
print(cipher.decode('ascii'))
