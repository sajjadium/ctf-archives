#!/usr/bin/env python3
import sys
import os


class ChaosStreamCipher:
    def __init__(self, key, r=3.9):
        if not 0 < key < 1:
            raise ValueError("Key must be a float in range (0, 1)")
        self.r = r
        self.x = key

    def _logistic_map(self):
        self.x = self.r * self.x * (1 - self.x)
        return self.x

    def _get_key_byte(self):
        x_next = self._logistic_map()
        key_byte = int(x_next * 256) % 256
        return key_byte

    def encrypt(self, plaintext):
        ciphertext = []
        for byte in plaintext:
            key_byte = self._get_key_byte()
            encrypted_byte = byte ^ key_byte
            ciphertext.append(encrypted_byte)
        return bytes(ciphertext)

    def decrypt(self, ciphertext):
        return self.encrypt(ciphertext)


def encrypt_file(input_path, output_path, key):
    if not os.path.exists(input_path):
        return False
    with open(input_path, 'rb') as f:
        plaintext = f.read()
    cipher = ChaosStreamCipher(key)
    ciphertext = cipher.encrypt(plaintext)
    with open(output_path, 'wb') as f:
        f.write(ciphertext)
    return True


def decrypt_file(input_path, output_path, key):
    if not os.path.exists(input_path):
        return False
    with open(input_path, 'rb') as f:
        ciphertext = f.read()
    cipher = ChaosStreamCipher(key)
    plaintext = cipher.decrypt(ciphertext)
    with open(output_path, 'wb') as f:
        f.write(plaintext)
    return True


def main():
    if len(sys.argv) < 4:
        print("Usage: python encrypt.py <input_file> <output_file> <key> [--decrypt]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    key = float(sys.argv[3])
    decrypt_mode = len(sys.argv) > 4 and sys.argv[4] == '--decrypt'

    if decrypt_mode:
        success = decrypt_file(input_file, output_file, key)
    else:
        success = encrypt_file(input_file, output_file, key)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
