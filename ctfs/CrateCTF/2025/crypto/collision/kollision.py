#!/usr/local/bin/python3

from collections.abc import Iterable
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from itertools import batched
from sys import stdin
from os import system

def xor(a: Iterable[int], b: Iterable[int]) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def hash(b: bytes) -> bytes:
    j = bytes([16] * 16)
    k = bytes([17] * 16)

    for chunk in batched(pad(b, 16), 16):
        j, k = k, xor(AES.new(j, AES.MODE_ECB).encrypt(bytes(chunk)), k)

    return k

texts = {}
if __name__ == "__main__":
    while True:
        match input("[v]alidate or [e]cho? "):
            case "v":
                print(end="> ", flush=True)
                text = stdin.buffer.readline().rstrip()
                texts[hash(text)] = all(c in "abcdefghijklmnopqrstuvwxyzåäö 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ.,/".encode() for c in text)
            case "e":
                print(end="> ", flush=True)
                text = stdin.buffer.readline().rstrip()
                if hash(text) in texts and texts[hash(text)] == True:
                    system(b"echo " + text)
                else:
                    print("👺")
