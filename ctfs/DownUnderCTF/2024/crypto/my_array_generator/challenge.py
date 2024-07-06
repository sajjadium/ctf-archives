#!/usr/bin/env python3
import random
import os

KEY = b"DUCTF{XXXXXXXXXXXXXXXXXXXXXXXXX}"
KEY_SIZE = 32
F = 2**14


class MyArrayGenerator:
    def __init__(self, key: bytes, n_registers: int = 128):
        self.key = key
        self.n_registers = n_registers

    def prepare(self):
        self.registers = [0 for _ in range(self.n_registers)]
        self.key_extension(self.key)

        self.carry = self.registers.pop()
        self.key_initialisation(F)

    def key_extension(self, key: bytes):
        if len(key) != KEY_SIZE:
            raise ValueError(f"Key length should be {KEY_SIZE} bytes.")

        for i in range(len(self.registers)):
            j = (4 * i) % KEY_SIZE
            subkey = key[j : j + 4]
            self.registers[i] = int.from_bytes(subkey)

    def key_initialisation(self, F: int):
        for _ in range(F):
            self.update()

    def shift(self):
        self.registers = self.registers[1:]

    def update(self):
        r0, r1, r2, r3 = self.registers[:4]

        self.carry ^= r1 if r2 > r3 else (r1 ^ 0xFFFFFFFF)

        self.shift()
        self.registers.append(self.registers[-1] ^ self.carry)

    def get_keystream(self) -> int:
        byte_index = random.randint(0, 3)
        byte_mask = 0xFF << (8 * byte_index)
        return (self.registers[-1] & byte_mask) >> (8 * byte_index)

    def encrypt(self, plaintext: bytes) -> bytes:
        self.prepare()

        ct = b""
        for b in plaintext:
            self.update()
            ct += int.to_bytes(self.get_keystream() ^ b)

        return ct

    def decrypt(self, ciphertext: bytes) -> bytes:
        return self.encrypt(ciphertext)


if __name__ == "__main__":
    random.seed(1234)
    cipher = MyArrayGenerator(KEY)

    plaintext = os.urandom(1280)
    print(f'plaintext = "{plaintext.hex()}"')

    ciphertext = cipher.encrypt(plaintext)
    print(f'ciphertext = "{ciphertext.hex()}"')
