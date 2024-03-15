#!/usr/bin/env python3

from Crypto.Hash import Poly1305
from Crypto.Cipher import ChaCha20
import os

N = 240
S = 10
L = 3
I = 13

with open("flag.txt", "rb") as f:
    flag = f.read().strip()

# "Poly1305 is a universal hash family designed by Daniel J. Bernstein for use in cryptography." - wikipedia
def poly1305_hash(data, Key, Nonce):
    hsh = Poly1305.new(key=Key, cipher=ChaCha20, nonce=Nonce)
    hsh.update(data=data)
    return hsh.digest()

# If i just use a hash function instead of a linear function in my LCG, then it should be super secure right?
class PolyCG:
    def __init__(self):
        self.Key = os.urandom(32)
        self.Nonce = os.urandom(8)
        self.State = os.urandom(16)

        # Oops.
        print("init = '" + poly1305_hash(b'init', self.Key, self.Nonce)[:I].hex() + "'")

    def next(self):
        out = self.State[S:S+L]
        self.State = poly1305_hash(self.State, self.Key, self.Nonce)
        return out

if __name__ == "__main__":
    pcg = PolyCG()
    v = []
    for i in range(N):
        v.append(pcg.next().hex())
    print(f'{v = }')

    key = b"".join([pcg.next() for _ in range(0, 32, L)])[:32]
    cipher = ChaCha20.new(key=key, nonce=b'\0'*8)
    flagenc = cipher.encrypt(flag)
    print(f"flagenc = '{flagenc.hex()}'")
