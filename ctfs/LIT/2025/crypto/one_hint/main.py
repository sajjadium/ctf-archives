#!/usr/bin/env python3
def vigenere(pt,key):
    res = ""
    for i in range(len(pt)):
        if pt[i] in "LITCTF{_}":
            res += pt[i]
            continue
        res += chr((ord(pt[i])+ord(key[i%len(key)])-2*ord('a'))%26+ord('a'))
    return res
def power(pt,n):
    a = pt
    for i in range(n):
        a = vigenere(a, vigenere(a, a))
    return a
flag = "LITCTF{redacted}"
print("hint 1: " + power(flag, 2345))
