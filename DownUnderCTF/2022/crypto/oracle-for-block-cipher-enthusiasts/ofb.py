#!/usr/bin/env python3

from os import urandom, path
from Crypto.Cipher import AES


FLAG = open(path.join(path.dirname(__file__), 'flag.txt'), 'r').read().strip()
MESSAGE = f'Decrypt this... {urandom(300).hex()} {FLAG}'


def main():
    key = urandom(16)
    for _ in range(2):
        iv = bytes.fromhex(input('iv: '))
        aes = AES.new(key, iv=iv, mode=AES.MODE_OFB)
        ct = aes.encrypt(MESSAGE.encode())
        print(ct.hex())


if __name__ == '__main__':
    main()
