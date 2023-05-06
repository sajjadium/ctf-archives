from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import md5
from os import urandom
from flag import flag

keys = [md5(urandom(3)).digest() for _ in range(2)]


def bytexor(da,ta): return bytes(i^j for i,j in zip(da,ta))


def get_ciphers(iv1, iv2):
    return [
        AES.new(keys[0], mode=AES.MODE_CBC, iv=iv1),
        AES.new(keys[1], mode=AES.MODE_CFB, iv=iv2, segment_size=8*16),
    ]

def encrypt(m: bytes, iv1: bytes, iv2: bytes) -> bytes:
    m = pad(m,32)
    ciphers = get_ciphers(iv1, iv2)
    c = m
    for cipher in ciphers:
        c = b''.join(i[16:]+bytexor(i[:16],cipher.encrypt(i[16:])) for i in [c[i:i+32] for i in range(0,len(c),32)])
    return c

plaintext = f'finally now i am able to send my secret with double security and double trust, {flag}'.encode()
iv1, iv2 = urandom(16),urandom(16)

ciphertext = encrypt(plaintext, iv1, iv2)
ciphertext = b":".join([x.hex().encode() for x in [iv1, iv2, ciphertext]])

open('encrypted','wb').write(ciphertext)