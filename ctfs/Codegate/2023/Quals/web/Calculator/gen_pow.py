#!/usr/bin/env python3
import secrets
import hashlib
from time import time

class NcPowser:
    def __init__(self, difficulty=28, prefix_length=22):
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
    prefix = powser.get_challenge()
    print(prefix)