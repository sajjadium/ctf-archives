from dataclasses import dataclass
from random import getrandbits

from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
from Crypto.Util.Padding import pad, unpad
from pwn import xor

from mvmcryption.crypto.rsa import RSA
from mvmcryption.utils import chunk

BLOCK_SIZE = 16


@dataclass
class SCBCCipher:
    """
    Scuffed CBC Cipher.

    If you're wondering why we aren't using CBC directly, this is part of our "Customer Retention Strategy".
    """

    key: bytes

    @property
    def _ecb(self):
        return AES.new(self.key, AES.MODE_ECB)

    def encrypt(self, plaintext: bytes, iv: bytes) -> bytes:
        padded = pad(plaintext, BLOCK_SIZE)
        enc = []
        blocks = chunk(padded)
        enc.append(self._ecb.encrypt(xor(blocks[0], iv)))

        for i, block in enumerate(blocks[1:]):
            enc.append(self._ecb.encrypt(xor(block, enc[i])))

        return b"".join(enc)

    def decrypt(self, ciphertext: bytes, iv: bytes) -> bytes:
        ndec = chunk(ciphertext)
        dec = []

        dec.append(xor(self._ecb.decrypt(ndec[0]), iv))

        for i, block in enumerate(ndec[1:]):
            dec.append(xor(self._ecb.decrypt(block), ndec[i]))

        return unpad(b"".join(dec), BLOCK_SIZE)
