from Crypto.Cipher import AES
from Crypto.Util.number import *
import os
from Crypto.Util.Padding import pad,unpad
from Crypto.Util.strxor import strxor
import random
import hashlib
from secrets import FLAG

KEY = os.urandom(16)
entropy = hashlib.md5(os.urandom(128)).digest()

def generate_token(username):
    iv = os.urandom(16)
    try:
        pt = bytes.fromhex(username)
    except:
        print("Invalid input.")
        exit(0)
    if b'gimmeflag' in pt:
        print("Nah not allowed.")
        exit(0)
    cipher = AES.new(KEY,AES.MODE_CBC,iv)
    ct = cipher.encrypt(pad(pt,16))
    tag = b'\x00'*16
    for i in range(0,len(ct),16):
        tag = strxor(tag,ct[i:i+16])
    tag = strxor(tag,iv)
    tag = strxor(tag,entropy)
    return tag.hex()+ct.hex()

def verify(tag,token):
    try:
        tag = bytes.fromhex(tag)
        ct = bytes.fromhex(token)
    except:
        print("Invalid input")
        exit(0)
    for i in range(0,len(ct),16):
        tag = strxor(tag,ct[i:i+16])
    tag = strxor(tag,entropy)
    iv = tag
    cipher = AES.new(KEY,AES.MODE_CBC,iv)
    username = cipher.decrypt(ct)
    return username.hex()

print("Hello new user")
print("We shall allow you to generate one token:")
print("Enter username in hex():")
username = input()
token = generate_token(username)
print(token)
while True:
    print("Validate yourself :)")
    print("Enter token in hex():")
    token = input()
    print("Enter tag in hex():")
    tag = input()
    if b'gimmeflag'.hex() in verify(tag,token):
        print("Oh no u flipped me...")
        print("I am now officially flipped...")
        print("Here's ur reward...")
        print(FLAG)
        break
    else:
        print("Something went wrong...")
        print(f"Is your username {verify(tag,token)}")
        print("Smthin looks fishy")
        print("Pls try again :(")
        print()
    entropy = hashlib.md5(entropy).digest()