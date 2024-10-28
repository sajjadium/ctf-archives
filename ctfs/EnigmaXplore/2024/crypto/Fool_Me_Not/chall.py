import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2


def multiply_bytes(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])


def aes_permutation(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(data)


def encrypt_keys(password, text, length=16):
    return PBKDF2(password, text, dkLen=length, count=1000000)


def encrypt(master_key, plaintext, num_rounds=3):
    important = os.urandom(16)
    k1 = encrypt_keys(plaintext, important, 16)
    k2 = encrypt_keys(plaintext, important[::-1], 16)
    termination_vector = os.urandom(16)
    intermediate = multiply_bytes(master_key, k1)
    for _ in range(num_rounds):
        intermediate = aes_permutation(intermediate, termination_vector)
        intermediate = multiply_bytes(intermediate, k2)
        intermediate = aes_permutation(intermediate, termination_vector)
        intermediate = multiply_bytes(intermediate, k1)

    return termination_vector + important + intermediate


k1 = 'REDACTED'
plaintext = 'REDACTED'
ciphertext = encrypt(plaintext.encode(), k1, num_rounds=5)
print("Ciphertext:", ciphertext)
# ciphertext = b'\xf9e\x8bgO\xab\x8co\xd5l\x91\xc9G\xf0+\xaa?\xe7\xa6\xd2\xa1\xc9:)\xef\xd0\xdd\x9a\xd5\xe8y/\xf70\xb2IM\xf2\x1a\x80\x1b\xb1\xea\xca\x1a\xecw\xb0'