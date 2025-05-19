#!/usr/local/bin/python

from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes
from secrets import FLAG

key = get_random_bytes(32)
nonce = get_random_bytes(8)

cipher = ChaCha20.new(key=key, nonce=nonce)
print(bytes.hex(cipher.encrypt(b'Slide to the left')))
print(bytes.hex(cipher.encrypt(b'Slide to the right')))

try:
    user_in = input().rstrip('\n')
    cipher = ChaCha20.new(key=key, nonce=nonce)
    decrypted = cipher.decrypt(bytes.fromhex(user_in))
    if decrypted == b'Criss cross, criss cross':
        print("Cha cha real smooth")
        print(FLAG)
    else:
        print("Those aren't the words!")
except Exception as e:
    print("Those aren't the words!")


