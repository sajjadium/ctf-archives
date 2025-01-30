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


@dataclass
class XSCBCCipher(SCBCCipher):
    """
    Extended Scuffed CBC Cipher.

    The same but with signatures, an (ex)-customer forced us to implement signatures for this after some of their users started abusing bit-flipping to insert commans and semicolons into all sorts of places.

    Our CISO somehow managed to keep this from going public, the general consesus is that he bribed the customer with some, well all the data, we shouldn't have but do. Ig sometimes stuff just works. See MVM-7173763 in Jira for more on this.
    """

    rsa: RSA

    def encrypt(self, plaintext: bytes) -> tuple[bytes, int]:
        iv = long_to_bytes(getrandbits(BLOCK_SIZE * 8), BLOCK_SIZE)
        ct = super().encrypt(plaintext, iv)
        signature = self.rsa.sign(iv + ct)
        # return ct, iv, signature
        return ct, signature

    def decrypt(self, ciphertext: bytes, signature: int, iv: bytes) -> bytes:
        if not self.rsa.verify(iv + ciphertext, signature):
            raise ValueError("Funny user.")
        return super().decrypt(ciphertext, iv)
