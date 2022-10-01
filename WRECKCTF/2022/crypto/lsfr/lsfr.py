#!/usr/local/bin/python

import random
from pylfsr import LFSR

with open ("flag.txt", "r") as f:
    flag = f.read()

def enc(plaintext):
    r = random.getrandbits(32)
    state = [int(i) for i in list(bin(r)[2:].zfill(32))]
    plaintext = list([int(j) for j in ''.join(format(ord(i), 'b').zfill(8) for i in plaintext)])
    l = LFSR(fpoly=[32,26,20,11,8,5,3,1], initstate=state)
    for i in range(0x1337):
        l.next()
    key = []
    for i in range(len(plaintext)):
        key.append(l.next())
    return "".join([str(plaintext[i]^key[i]) for i in range(len(plaintext))])

def menu():
    print("1. Encrypt Random String")
    print("2. Encrypt Flag")
    print("3. Exit")
    return input(">> ")

while True:
    choice = menu()
    if choice == "1":
        pt = input("Enter String: ")
        if len(pt)!=16:
            print("Invalid String Length")
            continue
        print(enc(pt))
    elif choice == "2":
        print(enc(flag))
        break
    elif choice == "3":
        break
    else:
        print("Invalid choice")
