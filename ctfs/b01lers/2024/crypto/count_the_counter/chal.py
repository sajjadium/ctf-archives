#!/bin/python3
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
from secret import flag
import os


def Encrypt(key, message, nonce):
    cipher = AES.new(key, AES.MODE_CTR, nonce=long_to_bytes(nonce))
    return cipher.encrypt(message).hex()


def chal():
    key = os.urandom(16)
    print("Treat or Trick, count my thing. ")
    nonce_counter = 1
    print(Encrypt(key, flag, nonce_counter))
    while True:
        nonce_counter += 1
        to_enc = input("Give me something to encrypt: ")
        print(Encrypt(key, bytes.fromhex(to_enc), nonce_counter))


if __name__ == "__main__":
    chal()
