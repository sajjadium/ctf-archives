from Crypto.Cipher import AES
from secret import flag
import os

kwargs = {"nonce": os.urandom(8)}
key = os.urandom(16)

def encrypt(msg):
    aes = AES.new(key, AES.MODE_CTR, **kwargs)
    return aes.encrypt(msg).hex()

print(encrypt(flag))
q = input("Encrypt this string:").encode()
print(encrypt(q))
