#!/usr/local/bin/python3

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

FLAG = open("flag.txt", "r").read().strip()

def encrypt(key, iv, plaintext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext, 16))
    return ciphertext

def decrypt(key, iv, ciphertext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), 16)
    return plaintext

def encode(data):
    return b", ".join([str(ord(b)).encode() for b in data])

def decode(data):
    return "".join([chr(int(b)) for b in data.split(b",")])

def handle():
    assert len(FLAG) == 44
    assert FLAG.startswith("ifctf{")
    print("Welcome to the service!")

    with open("key", "rb") as f:
        key = f.read()

    while True:
        try:
            iv = os.urandom(16)
            print("encrypt or check?")
            cmd = input("cmd: ")
            if cmd == "encrypt":
                name = input("name: ")
                if len(name) > 10 or name == "admin" or "flag" in name:
                    print("We don't do that here...")
                    exit()
                tag = f"name:{name}"
                ciphertext = encrypt(key, iv, encode(tag))
                print("tag: ", ciphertext.hex())
            elif cmd == "check":
                tag = bytes.fromhex(input("tag: "))
                iv_ = input("iv: ")
                if len(iv_) == 32:
                    iv = bytes.fromhex(iv_)
                tag = decrypt(key, iv, tag)
                tag = decode(tag)
                cmds = tag.split(",")
                if (",flag:" not in tag) and (cmds[0] == "name:admin") and (cmds[1] == "cmd:getflag") and (cmds[2] == "psw:superpassword"):
                    print("wow, you are admin!")
                    tag+=f",flag:{FLAG}"
                ciphertext = encrypt(key, iv, encode(tag))
                print("tag: ", ciphertext.hex())
        except:
            pass

if __name__ == '__main__':
    handle()
