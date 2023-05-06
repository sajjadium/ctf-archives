import base64
import json
import random
import sys
import os

from Crypto.Util.number import isPrime
from Crypto.Cipher import AES

RSA_KEY_SZ = 256
AES_KEY_SZ = 128


class AuthEncryption:
    def __init__(self, key: bytes):
        self._rand = random.Random(key)
        mask = (0b11 << (RSA_KEY_SZ // 2 - 2)) | 1
        p = q = 0
        while not isPrime(p):
            p = self._rand.getrandbits(RSA_KEY_SZ // 2) | mask
        while not isPrime(q):
            q = self._rand.getrandbits(RSA_KEY_SZ // 2) | mask
        self.n = p * q
        assert self.n.bit_length() == RSA_KEY_SZ
        self.exp = self._rand.getrandbits(RSA_KEY_SZ)
        self.aes_key = self._rand.randbytes(AES_KEY_SZ // 8)

    def _generate_signature(self, data: bytes) -> bytes:
        msg = int.from_bytes(data, "big")
        sig = pow(msg, self.exp, self.n)
        return sig.to_bytes(RSA_KEY_SZ // 8, "big")

    def _verify_signature(self, data: bytes, sig: bytes) -> bool:
        msg = int.from_bytes(data, "big")
        s = int.from_bytes(sig, "big")
        if s >= self.n:
            print("[warning: sig >= modulo]", end=' ')
            s %= self.n
        return pow(msg, self.exp, self.n) == s

    def _xxcrypt(self, data: bytes) -> bytes:
        aes = AES.new(self.aes_key, AES.MODE_CTR, nonce=b'\x00' * 12)
        return aes.encrypt(data)

    def encrypt(self, plaintext: bytes) -> bytes:
        sig = self._generate_signature(plaintext)
        return self._xxcrypt(plaintext + sig)

    def decrypt(self, data: bytes) -> bytes:
        decrypted = self._xxcrypt(data)
        plaintext, sig = decrypted[:-RSA_KEY_SZ // 8], decrypted[-RSA_KEY_SZ // 8:]
        assert self._verify_signature(plaintext, sig), "integrity verification failed"
        return plaintext


if __name__ == '__main__':
    from secret import FLAG

    encryptor = AuthEncryption(os.urandom(16))
    m = b'{"name": "admin", "admin": true, "issued_date": "01/01/2023"}'
    assert encryptor.decrypt(encryptor.encrypt(m)) == m, "sanity check failed"

    for _ in range(16000):
        try:
            token = encryptor.decrypt(base64.b64decode(input()))
            info = json.loads(token)
            if info["admin"]:
                print(f"Somehow the sanity-check token is leaked, token={info}", file=sys.stderr)
                print(FLAG)
            else:
                print(f"Hi {info['name']}")
        except Exception as err:
            print(err)
