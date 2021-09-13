#!/usr/bin/env python3
import sys
import os
import random
import binascii
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes, bytes_to_long
from secret import FLAG

IV = os.urandom(AES.block_size)
KEY = os.urandom(AES.block_size)

class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)

def pad(msg):
    return msg + (chr(16 - len(msg) % 16) * (16 - len(msg) % 16)).encode()

def get_flag():
    flag = pad(FLAG)
    cipher = AES.new(IV, AES.MODE_ECB)
    flag = cipher.encrypt(flag)

    enc = b''
    flag = pad(flag)
    iv = IV
    for i in range(0, len(flag), 16):
        cipher = AES.new(KEY, AES.MODE_CBC, iv)
        enc += cipher.encrypt(flag[i:i+16])
        iv = long_to_bytes(bytes_to_long(enc[i:i+16]) ^ bytes_to_long(flag[i:i+16]))
    print('flag (in hex) =', binascii.hexlify(enc).decode())

def encrypt():
    msg = input('msg (in hex) = ')
    if (len(msg) % 2 != 0):
        print('Invalid input!')
        return
    msg = binascii.unhexlify(msg.encode())
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    enc = cipher.encrypt(pad(msg))
    print('enc (in hex) =', binascii.hexlify(enc).decode())

def decrypt():
    enc = input('enc (in hex) = ')
    if (len(enc) % 32 != 0):
        print('Invalid input!')
        return
    enc = binascii.unhexlify(enc.encode())
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    msg = cipher.decrypt(enc)
    print('msg (in hex) =', binascii.hexlify(msg).decode())

def menu():
    print('1. Get encrypted flag')
    print('2. Encrypt a message')
    print('3. Decrypt a message')
    print('4. Exit')

if __name__ == '__main__':
    while True:
        try:
            menu()
            choice = input('> ')
            if choice == '1':
                get_flag()
            elif (choice == '2'):
                encrypt()
            elif (choice == '3'):
                decrypt()
            elif (choice == '4'):
                print('Bye.')
                break
            else:
                print('Invalid input!')
        except:
            print('Something went wrong.')
            break
