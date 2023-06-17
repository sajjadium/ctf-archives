#!/usr/bin/env python3
from file_crypto import FileCipher, random_index, index_to_bytes, index_from_bytes
from file_crypto import LOCAL_NONCE, BLOCK_SIZE, INDEX_SIZE

import sys

if __name__ == "__main__":
    assert len(sys.argv) == 3

    cipher = FileCipher()
    with open(sys.argv[2], "rb") as f:
        data = f.read()

    if sys.argv[1] == "enc":
        index = random_index()
        ciphertext = cipher.encrypt(LOCAL_NONCE, index, data)
        index_bytes = index_to_bytes(index)

        with open(sys.argv[2] + ".enc", "wb") as f:
            f.write(LOCAL_NONCE)
            f.write(index_bytes)
            f.write(ciphertext)

    elif sys.argv[1] == "dec":
        nonce = data[:BLOCK_SIZE]
        index_bytes = data[BLOCK_SIZE : BLOCK_SIZE + INDEX_SIZE]
        ciphertext = data[BLOCK_SIZE + INDEX_SIZE :]

        index = index_from_bytes(index_bytes)
        plaintext = cipher.decrypt(nonce, index, ciphertext)

        with open(sys.argv[2] + ".dec", "wb") as f:
            f.write(plaintext)
