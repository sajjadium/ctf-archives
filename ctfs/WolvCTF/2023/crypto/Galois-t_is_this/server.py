#!/usr/bin/python3
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.number import *
from Crypto.Util.strxor import *
import os
from pathlib import Path

def GF_mult(x, y):
    product = 0
    for i in range(127, -1, -1):
        product ^= x * ((y >> i) & 1)
        x = (x >> 1) ^ ((x & 1) * 0xE1000000000000000000000000000000)
    return product

def H_mult(H, val):
    product = 0
    for i in range(16):
        product ^= GF_mult(H, (val & 0xFF) << (8 * i))
        val >>= 8
    return product

def GHASH(H, A, C):
    C_len = len(C)
    A_padded = bytes_to_long(A + b'\x00' * (16 - len(A) % 16))
    if C_len % 16 != 0:
        C += b'\x00' * (16 - C_len % 16)

    tag = H_mult(H, A_padded)

    for i in range(0, len(C) // 16):
        tag ^= bytes_to_long(C[i*16:i*16+16])
        tag = H_mult(H, tag)

    tag ^= bytes_to_long((8*len(A)).to_bytes(8, 'big') + (8*C_len).to_bytes(8, 'big'))
    tag = H_mult(H, tag)

    return tag

FLAG = Path('flag.txt').read_text()

# 128-bit blocks
AES_BLOCK_SIZE = 16
key = get_random_bytes(16)
header = b'WolvCTFCertified'
message = b'heythisisasupersecretsupersecret'
used_nonces = set()

def incr(counter):
    temp = bytes_to_long(counter)
    return long_to_bytes(temp + 1, 16)[-16:]

def check_nonce(nonce):
    # if you can't reuse the nonce, surely you can't explot this oracle!
    if(nonce in used_nonces):
        print("Sorry, a number used once can't be used twice!")
        exit(0)
    used_nonces.add(nonce)

def encrypt(nonce, pt):
    pt = bytes.fromhex(pt)
    assert(len(pt) % 16 == 0)
    numBlocks = len(pt) // AES_BLOCK_SIZE
    if(numBlocks > 3):
        print("Sorry, we just don't have the resources to encrypt a message that long!")
        exit(0)

    nonce = bytes.fromhex(nonce)
    assert(len(nonce) == 16)
    check_nonce(nonce)

    cipher = AES.new(key, AES.MODE_ECB)
    hkey = cipher.encrypt(b'\0' * 16)
    enc = b''
    for i in range(numBlocks + 1):
        enc += cipher.encrypt(nonce)
        # the counter is just the nonce, right? right??
        nonce = incr(nonce)

    ct = b''
    for i in range(1, numBlocks + 1):
        ct += strxor(
            enc[i * AES_BLOCK_SIZE: (i+1) * AES_BLOCK_SIZE],
            pt[(i-1) * AES_BLOCK_SIZE: i * AES_BLOCK_SIZE])
        
    authTag = strxor(
        enc[:AES_BLOCK_SIZE],
        long_to_bytes(GHASH(bytes_to_long(hkey), header, ct)))
    
    return ct.hex(), authTag.hex()

def decrypt(nonce, ct, tag):
    ct = bytes.fromhex(ct)
    assert(len(ct) % 16 == 0)
    numBlocks = len(ct) // AES_BLOCK_SIZE

    nonce = bytes.fromhex(nonce)
    assert(len(nonce) == 16)
    check_nonce(nonce)

    tag = bytes.fromhex(tag)
    assert(len(tag) == 16)

    cipher = AES.new(key, AES.MODE_ECB)
    hkey = cipher.encrypt(b'\0' * 16)
    enc = b''
    for i in range(numBlocks + 1):
        enc += cipher.encrypt(nonce)
        # the counter is just the nonce, right?
        nonce = incr(nonce)

    pt = b''
    for i in range(1, numBlocks + 1):
        pt += strxor(
            enc[i * AES_BLOCK_SIZE: (i+1) * AES_BLOCK_SIZE],
            ct[(i-1) * AES_BLOCK_SIZE: i * AES_BLOCK_SIZE])
        
    authTag = strxor(
        enc[:AES_BLOCK_SIZE],
        long_to_bytes(GHASH(bytes_to_long(hkey), header, ct)))

    if(pt == message):
        if(authTag == tag):
            print(FLAG)
        else:
            print("Whoops, that doesn't seem to be authentic!")
    else:
        print("Hmm, that's not the message I was looking for...")

MENU = """
1. Encrypt
2. Submit
3. Exit
"""

def main():
    print("If you can send me a valid super secret super secret I'll give you a reward!")
    while len(used_nonces) < 3:
        print(MENU)
        command = input("> ")
        match command:
            case "1":
                nonce = input("IV (hex) > ")
                pt = input("Plaintext (hex) > ")
                ct, tag = encrypt(nonce, pt)
                
                print("CT: ", ct)
                print("TAG: ", tag)
            case "2":
                nonce = input("IV (hex) > ")
                ct = input("Ciphertext (hex) > ")
                tag = input("Tag (hex) > ")
                decrypt(nonce, ct, tag)
                exit(0)
            case other:
                print("Bye!")
                exit(0)
    print("I know encryption is fun, but you can't just keep doing it...")
        
if __name__ == "__main__":
    main()