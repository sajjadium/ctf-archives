#!/usr/bin/env python3
import math
import binascii
from Crypto.Util.Padding import pad, unpad


print("""
Welcome to the official communication encryption system for rainbow bridges.
Input the encryption password given to you by your sponsor diety to encode messages,
and use the decryption password given to you to decode messages.
""")

def encode_block(m, pm):
    m = [i for i in m]
    c = [0] * 16
    for i, w in enumerate(pm):
        for j, l in enumerate(w):
            if l == '1':
                c[j] ^= m[i]
    return binascii.hexlify(bytes(c))
        

def encode(m, pwd):
    pm = []
    while pwd:
      a = '0'*8 + bin(ord(pwd[0]))[2:]
      a = a[-8:]
      b = '0'*8 + bin(ord(pwd[1]))[2:]
      b = b[-8:]
      pm.append(a + b)
      pwd = pwd[2:]
    c = b""
    while m:
        c += encode_block(m[:16], pm)
        m = m[16:]
    return c

while True:
    print("Would you like to encrypt (E), decrypt (D), or quit (Q)?")
    l = input(">>> ").strip().upper()
    if (len(l) > 1):
        print("You inputted more than one character...")
    elif (l == "Q"):
        print("Don't forget to perform sacrifices for your sponsor diety daily!")
        exit()
    elif (l == "E"):
        print("What is your encryption password?")
        pwd = input(">>> ").strip()
        assert len(pwd) == 32
        print("What would you like to encrypt?")
        m = input(">>> ").strip()
        c = encode(pad(m.encode('ascii'), 16), pwd)
        print("Here's your encoded message:")
        print(c)
    elif (l == "D"):
        print("Oops, for now, that feature is reserved for your sponsor diety.")
