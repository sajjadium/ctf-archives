#!/usr/local/bin/python3

import hmac
from os import urandom

def strxor(a: bytes, b: bytes):
    return bytes([x ^ y for x, y in zip(a, b)])

class Cipher:
    def __init__(self, key: bytes):
        self.key = key
        self.block_size = 16
        self.rounds = 1

    def F(self, x: bytes):
        return hmac.new(self.key, x, 'md5').digest()[:15]

    def encrypt(self, plaintext: bytes):
        plaintext = plaintext.ljust(self.block_size, b'\x00')
        ciphertext = b''

        for i in range(0, len(plaintext), self.block_size):
            block = plaintext[i:i+self.block_size]
            for _ in range(self.rounds):
                L, R = block[:-1], block[-1:]
                L, R = R, strxor(L, self.F(R))
                block = L + R
            ciphertext += block

        return ciphertext


key = urandom(16)
cipher = Cipher(key)
flag = open('flag.txt', 'rb').read().strip()

print("faked onion")
while True:
    choice = input("1. Encrypt a message\n2. Get encrypted flag\n3. Exit\n> ").strip()

    if choice == '1':
        pt = input("Enter your message in hex: ").strip()
        pt = bytes.fromhex(pt)
        print(cipher.encrypt(pt).hex())
    elif choice == '2':
        print(cipher.encrypt(flag).hex())
    else:
        break

print("Goodbye!")