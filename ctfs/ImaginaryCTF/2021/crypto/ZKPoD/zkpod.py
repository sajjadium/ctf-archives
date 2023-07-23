#!/usr/local/bin/python
from Crypto.Util.number import bytes_to_long, getRandomRange
import hashlib

N = 0xbb00128c1c1555dc8fc1cd09b3bb2c3efeaae016fcb336491bd022f83a10a501175c044843dbec0290c5f75d9a93710246361e4822331348e9bf40fc6810d5fc7315f37eb8f06fb3f0c0e9f63c2c207c29f367dc45eef2e5962eff35634b7a29d913a59cd0918fa395571d3901f8abd83322bd17b60fd0180358b7e36271adcfc1f9105b41da6950a17dba536a2b600f2dc35e88c4a9dd208ad85340de4d3c6025d1bd6e03e9449f83afa28b9ff814bd5662018be9170b2205f38cf3b67ba5909c81267daa711fcdb8c7844bbc943506e33f5f72f603119526072efbc5ceae785f2af634e6c7d2dd0d51d6cfd34a3bc2b15a752918d4090d2ca253df4ef47b8b
e = 0x10001
P = 0x199e1926f2d2d5967b1d230b33de0a249f958e5b962f8b82ca042970180fe1505607fe4c8cde04bc6d53aec53b4aa25255ae67051d6ed9b602b1b19e128835b20227db7ee19cf88660a50459108750f8b96c71847e4f38a79772a089aa46666404fd671ca17ea36ee9f401b4083f9ca76f5217588c6a15baba7eb4a0934e2026937812c96e2a5853c0e5a65231f3eb9fdc283e4177a97143fe1a3764dc87fd6d681f51f49f6eed5ab7ddc2a1da7206f77b8c7922c5f4a5cfa916b743ceeda943bc73d821d2f12354828817ff73bcd5800ed201c5ac66fa82df931c5bbc76e03e48720742ffe673b7786e40f243d7a0816c71eb641e5d58531242f7f5cfef60e5b
g = 2

with open("flag.txt", "rb") as f:
    flag = bytes_to_long(f.read().strip())
    assert flag < N

with open("private.txt", "r") as f:
    d = int(f.read().strip())

def decrypt(c):
    return pow(c, d, N)

def H(x):
    return bytes_to_long(hashlib.sha512(b"domain" + x).digest() + hashlib.sha512(b"separation" + x).digest())

def sign(x):
    k = getRandomRange(0, P - 1)
    r = pow(g, k, P)
    e = H(str(r).encode() + b"Haha, arbitrary message")
    s = (k - x * e) % (P - 1)
    return r, s

print(f"Here's my encrypted flag: {hex(pow(flag, e, N))}")
print("To prove that I can correctly decrypt whatever you send to me, I'll use decryptions to sign messages")
while True:
    print("> ", end="")
    c = int(input(), 16)
    m = decrypt(c)
    r, s = sign(m)
    print(f"r: {r}")
    print(f"s: {s}")
