from Crypto.Util.number import *
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import os
import base64
from hashlib import sha256
from secret import flag

# LFSR template by Cryptanalyse
class StreamCipher:
    def __init__(self, key):
        assert len(key) == 128, "Error: the key must be of exactly 128 bits."
        self._s = key
        self._t = [0, 1, 2, 7]
        self._p = [0, 8, 16, 32, 64, 120]
        self._f = [[0], [2], [3], [5], [0, 1], [0, 3], [1, 4], [2, 3],\
        		   [0, 1, 4], [2, 3, 4], [0, 1, 2, 4, 5], [1, 2, 3, 4, 5]]

    def _prod(self, L):
        return all(x for x in L)

    def _sum(self, L):
        return sum(L) & 1

    def _clock(self):
        x = [self._s[p] for p in self._p]
        self._s = self._s[1:] + [self._sum(self._s[p] for p in self._t)]
        return self._sum(self._prod(x[v] for v in m) for m in self._f)

    def keystream(self, size):
        c = []
        for i in range(size):
            b = 0
            for _ in range(8):
                b = (b << 1) | self._clock()
            c += [b]
        return bytes(c)

key = os.urandom(16)
lfsr = StreamCipher(list(map(int, list(f"{bytes_to_long(key):0128b}"))))
ks = lfsr.keystream(1 << 10)

cipher = AES.new(key, AES.MODE_CBC, iv=b"\0" * 16)
ciphertext = cipher.encrypt(pad(flag, 16))

f = open("out.txt", "w")
f.write(base64.b64encode(ks).decode("ascii") + "\n" + ciphertext.hex())
