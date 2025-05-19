#!/usr/local/bin/python

import encrypt

key = encrypt.getRandomKey()
flag = open("flag.txt").read().strip().split("byuctf{")[1].split("}")[0]


flag = [letter.lower() for letter in flag if letter.isalpha()]
print(encrypt.encrypt(flag, key))


for _ in range(20):
    plaintext = input("What to encrypt:\n")
    plaintext = [letter.lower() for letter in plaintext if letter.isalpha()]

    if plaintext == "":
        break
    
    print(encrypt.encrypt(plaintext, key))