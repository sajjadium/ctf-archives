#!/usr/bin/env python3

import os
import sys

MESSAGE_SIZE = 8
TAG_SIZE = 16

class CRYSig:
    def __init__(self):
        # 128 * 64 matrix of 0 and 1s
        self.matrix = []
        for _ in range(TAG_SIZE * 8):
            self.matrix.append(int.from_bytes(os.urandom(MESSAGE_SIZE)))

    def sign(self, message: bytes) -> bytes:
        if len(message) != MESSAGE_SIZE:
            raise ValueError(f"message must be exactly {MESSAGE_SIZE} bytes")

        # 64 bit column vector from message
        msg_vector = int.from_bytes(message)

        res = 0
        # valuate self.matrix * [message]
        for row in self.matrix:
            res <<= 1
            res += (row & msg_vector).bit_count() % 2

        return res.to_bytes(TAG_SIZE)

    def verify(self, message: bytes, signature: bytes) -> bool:
        if len(signature) != TAG_SIZE:
            return False

        try:
            return self.sign(message) == signature
        except ValueError:
            return False


if __name__ == "__main__":
    sig = CRYSig()

    # users
    user = b"babyuser"
    root = b"chadr00t"

    user_sig = sig.sign(user)

    print(f"user signature: {user_sig.hex()}")

    # query
    query = bytes.fromhex(input("> "))

    if query == root:
        print("holy cheating")
        sys.exit(0)

    query_sign = sig.sign(query)
    print(f"your signature: {query_sign.hex()}")

    # try get root
    attempt = input("> ")
    if sig.verify(root, bytes.fromhex(attempt)):
        with open("/flag") as f:
            print(f.read())
    else:
        print("rip")
