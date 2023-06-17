#!/usr/bin/env python3
import secrets
import hashlib
from time import time
import sys

class NcPowser:
    def __init__(self, difficulty=22, prefix_length=16):
        self.difficulty = difficulty
        self.prefix_length = prefix_length

    def get_challenge(self):
        return secrets.token_urlsafe(self.prefix_length)[:self.prefix_length].replace('-', 'b').replace('_', 'a')

    def verify_hash(self, prefix, answer):
        h = hashlib.sha256()
        h.update((prefix + answer).encode())
        bits = ''.join(bin(i)[2:].zfill(8) for i in h.digest())
        return bits.startswith('0' * self.difficulty)

if __name__ == '__main__':
    powser = NcPowser()
    if powser.verify_hash(sys.argv[1],sys.argv[2]):
        print("success")
    else:
        print("fail")