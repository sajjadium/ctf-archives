#!/usr/bin/env -S python3 -u
import os
import threading
import sys
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from binascii import hexlify

os.chdir(os.path.dirname(__file__))
KEY = open("server.key", "rb").read()
FLAG_TXT = open("flag.txt").read()
FLAG_ENC = open("flag.enc").read()

class PaddingError(Exception):
    pass

class CipherTextFormatError(Exception):
    pass

class Cipher:
    def __init__(self, key: bytes):
        self._key = key

    def encrypt(self, message: str) -> str:
        aes = AES.new(self._key, AES.MODE_OFB, iv=get_random_bytes(AES.block_size))
        ciphertext = aes.encrypt(pad(message.encode(), AES.block_size))

        return hexlify(aes.iv + ciphertext).decode()

    def decrypt(self, message: str) -> str:
        ciphertext_bytes = self._get_hex_bytes(message)
        iv, ciphertext = ciphertext_bytes[0:AES.block_size], ciphertext_bytes[AES.block_size:]
        aes = AES.new(self._key, AES.MODE_OFB, iv=iv)
        plaintext = aes.decrypt(ciphertext)
        plaintext_unpad = self._unpad(plaintext)

        return plaintext_unpad.decode()

    @staticmethod
    def _get_hex_bytes(ciphertext: str) -> bytes:
        try:
            if len(ciphertext) % AES.block_size != 0:
                raise CipherTextFormatError()
            return bytes.fromhex(ciphertext)
        except ValueError:
            raise CipherTextFormatError()

    @staticmethod
    def _unpad(plaintext: bytes) -> bytes:
        try:
            return unpad(plaintext, AES.block_size)
        except ValueError:
            raise PaddingError()

cipher = Cipher(KEY)

def handle() -> None:
    print(f"Welcome {os.getenv('SOCAT_PEERADDR', '')}")
    print(f"Encrypted flag: {FLAG_ENC}")
    while True:
        ciphertext = input("Enter a ciphertext you want to decrypt: ").rstrip()
        if not ciphertext:
            break

        try:
            flag_dec = cipher.decrypt(ciphertext)
            if flag_dec == FLAG_TXT:
                print(f"Flag: {flag_dec}")
            else:
                print("Padding correct!")

        except PaddingError:
            print("Padding incorrect!")
        except (CipherTextFormatError, UnicodeDecodeError):
            print("Invalid message format!")

def main() -> None:
    assert len(KEY) in AES.key_size
    assert len(FLAG_ENC) % AES.block_size == 0
    handle()

if __name__ == "__main__":
    main()
