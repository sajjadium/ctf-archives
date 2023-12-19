#!/usr/bin/python3 -u

import json
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from ecdsa import VerifyingKey
from ecdsa.util import sigdecode_der
from random import getrandbits
from secret import FLAG

with open("public.pem") as f:
    public_key = VerifyingKey.from_pem(f.read())

with open("users.json", 'r') as f:
    users = json.load(f)

def verify(name, userid, sig):
    msg = f'{name} | {userid}'.encode()
    try:
        return public_key.verify(sig, msg, hashlib.sha256, sigdecode=sigdecode_der)
    except:
        print(f"signature verification failed")
        return False

def iv_gen():
    iv = b''.join(getrandbits(24).to_bytes(3, byteorder='big') for i in range(4))
    return iv + b'nite'

def encrypt(key, pt):
    iv = iv_gen()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(pt, AES.block_size))
    return iv + ct

def decrypt(key, ct):
    iv = ct[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct[16:]), AES.block_size)
    return pt.decode()

def get_flag():
    key = getrandbits(128).to_bytes(16, byteorder='big')
    return encrypt(key, FLAG)

def login():
    print("\nenter credentials:")
    name = input("name: ")
    userid = input("userid: ")
    sig = input("signature: ")
    
    if verify(name, userid, bytes.fromhex(sig)):
        if (name == "FUTURE ADMIN" and userid == "SONY953"):
            admin()
        else:
            try:
                assert users[userid]['sign'] == sig
            except:
                print("invalid credentials")
            user()
    else:
        print("invalid credentials")

def user():
    while True:
        print("\nchoose an option:")
        print("1. encrypt\n2. decrypt\n3. back to login\n4. exit")
        option = input(">> ")
        if option == "1":
            key_hex = input("key (hex): ")
            pt = input("plaintext: ")
            try:
                key = bytes.fromhex(key_hex)
                assert len(key) == 16
                ct = encrypt(key, pt.encode())
                print(f"encrypted: {ct.hex()}")
            except Exception as e:
                print(f"error encrypting: {e}")
        elif option == "2":
            key_hex = input("key (hex): ")
            ct = input("ciphertext (hex): ")
            try:
                key = bytes.fromhex(key_hex)
                assert len(key) == 16
                pt = decrypt(key, bytes.fromhex(ct))
                print(f"decrypted: {pt}")
            except Exception as e:
                print(f"error decrypting: {e}")
        elif option == "3":
            break
        elif option == "4":
            exit()

def admin():
    while True:
        print("\nchoose an option:")
        print("1. get flag\n2. back to login\n3. exit")
        option = input(">> ")
        if option == "1":
            flag = get_flag()
            print(f"\nencrypted: {flag.hex()}")
        elif option == "2":
            break
        elif option == "3":
            exit()

def main():
    while True:
        login()

if __name__ == "__main__":
    main()
