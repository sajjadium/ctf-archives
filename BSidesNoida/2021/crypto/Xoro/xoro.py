#!/usr/bin/env python3
import os

FLAG = open('flag.txt','rb').read()

def xor(a, b):
    return bytes([i^j for i,j in zip(a,b)])

def pad(text, size):
    return text*(size//len(text)) + text[:size%len(text)]

def encrypt(data, key):
    keystream = pad(key, len(data))
    encrypted = xor(keystream, data)
    return encrypted.hex()


if __name__ == "__main__":
    print("\n===== WELCOME TO OUR ENCRYPTION SERVICE =====\n")
    try:
        key = os.urandom(32)
        pt = input('[plaintext (hex)]>  ').strip()
        ct = encrypt(bytes.fromhex(pt) + FLAG, key)
        print("[ciphertext (hex)]>", ct)
        print("See ya ;)")
    except Exception as e:
        print(":( Oops!", e)
        print("Terminating Session!")