#!/usr/local/bin/python

from Crypto.Util.number import *
p = getPrime(1024)
q = getPrime(1024)
n = p * q
e = 65537
flag = open('flag.txt', 'rb').read()
d = inverse(e, (p-1)*(q-1))

pandaman = b"PANDAMAN! I LOVE PANDAMAN! PANDAMAN MY BELOVED! PANDAMAN IS MY FAVORITE PERSON IN THE WHOLE WORLD! PANDAMAN!!!!"

def enc(m):
    if pandaman == m:
        return "No :("
    else:
        return pow(bytes_to_long(m), d, n)

def check():
    if long_to_bytes(pow(int(input("Enter here: ")), e, n)) == pandaman:
        print(flag)
    else:
        print("darn :(")

def menu():
    print("1. Encrypt")
    print("2. Check")
    print("3. Exit")
    return input(">> ")

while True:
    choice = menu()
    if choice == "1":
        pt = input("Enter String: ")
        print(enc(pt.encode('utf-8')))
    elif choice == "2":
        check()
    elif choice == "3":
        break
    else:
        print("Invalid choice")
