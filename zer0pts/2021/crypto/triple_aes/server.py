from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from binascii import hexlify, unhexlify
from hashlib import md5
import os
import signal
from flag import flag

keys = [md5(os.urandom(3)).digest() for _ in range(3)]


def get_ciphers(iv1, iv2):
    return [
        AES.new(keys[0], mode=AES.MODE_ECB),
        AES.new(keys[1], mode=AES.MODE_CBC, iv=iv1),
        AES.new(keys[2], mode=AES.MODE_CFB, iv=iv2, segment_size=8*16),
    ]

def encrypt(m: bytes, iv1: bytes, iv2: bytes) -> bytes:
    assert len(m) % 16 == 0
    ciphers = get_ciphers(iv1, iv2)
    c = m
    for cipher in ciphers:
        c = cipher.encrypt(c)
    return c

def decrypt(c: bytes, iv1: bytes, iv2: bytes) -> bytes:
    assert len(c) % 16 == 0
    ciphers = get_ciphers(iv1, iv2)
    m = c
    for cipher in ciphers[::-1]:
        m = cipher.decrypt(m)
    return m

signal.alarm(3600)
while True:
    print("==== MENU ====")
    print("1. Encrypt your plaintext")
    print("2. Decrypt your ciphertext")
    print("3. Get encrypted flag")
    choice = int(input("> "))

    if choice == 1:
        plaintext = unhexlify(input("your plaintext(hex): "))
        iv1, iv2 = get_random_bytes(16), get_random_bytes(16)
        ciphertext = encrypt(plaintext, iv1, iv2)
        ciphertext = b":".join([hexlify(x) for x in [iv1, iv2, ciphertext]]).decode()
        print("here's the ciphertext: {}".format(ciphertext))

    elif choice == 2:
        ciphertext = input("your ciphertext: ")
        iv1, iv2, ciphertext = [unhexlify(x) for x in ciphertext.strip().split(":")]
        plaintext = decrypt(ciphertext, iv1, iv2)
        print("here's the plaintext(hex): {}".format(hexlify(plaintext).decode()))

    elif choice == 3:
        plaintext = flag
        iv1, iv2 = get_random_bytes(16), get_random_bytes(16)
        ciphertext = encrypt(plaintext, iv1, iv2)
        ciphertext = b":".join([hexlify(x) for x in [iv1, iv2, ciphertext]]).decode()
        print("here's the encrypted flag: {}".format(ciphertext))
        exit()

    else:
        exit()
