#!/usr/bin/env python3
from file_crypto import FileCipher, random_index, index_from_bytes
from file_crypto import LOCAL_NONCE

import base64

if __name__ == "__main__":
    # Read data
    mode = input("mode? ").strip()
    nonce = base64.b64decode(input("nonce? ").strip())
    index_bytes = base64.b64decode(input("index? ").strip())
    data = base64.b64decode(input("data? ").strip())

    if len(data) > 0x4000:
        print("Sorry, the length of the given data is too long :(")
        exit(1)

    if nonce == LOCAL_NONCE:
        print("Sorry, this nonce is only allowed in the local mode :(")
        exit(1)

    # Do crypto
    cipher = FileCipher()
    index = index_from_bytes(index_bytes)
    if mode == "enc":
        result = cipher.encrypt(nonce, index, data)
    elif mode == "dec":
        result = cipher.decrypt(nonce, index, data)
    else:
        print("Wrong mode! :(")
        exit(1)
    print(base64.b64encode(result).decode())
