#!/usr/bin/env python3

from aes import AES
import sys

key = <REDACTED>

while True:
    print("plaintext hex string: ", end="")
    msg = bytes.fromhex(input())
    if len(msg) % 16 != 0:
        msg += b"\x00"*(16 - (len(msg) % 16))

    ciphertext = b""
    aes = AES()
    for i in range(0, len(msg), 16):
        msgblock = msg[i:i+16]
        cipherblock = bytes(aes.encrypt(msgblock, key, 16))
        ciphertext += cipherblock

    print(ciphertext.hex())
