from AES import encrypt, pad
from redacted import secret, flag, EXIT
import json
import os

plaintext = pad(flag, 16)

for _ in range(10):
    iv = os.urandom(8)*2
    key = os.urandom(16) 
    try:
        ciphertext = encrypt(key, plaintext, mode="CBC", iv=iv)
    except:
        EXIT()
    print(json.dumps({
        'key': key.hex(),
        'ciphertext': ciphertext.hex()
    }))
    inp = input("Enter iv: ")
    if (iv.hex() != inp):
        EXIT()
    print()

plaintext = pad(secret, 16)
iv = os.urandom(8)*2
key = os.urandom(16)
try:
    ciphertext = encrypt(key, plaintext, mode="CBC", iv=iv) 
except:
    EXIT()
print(json.dumps({
    'key': key.hex(),
    'ciphertext': ciphertext.hex()
}))
