import os
import signal
from Crypto.Cipher import ARC4
import string
import random

signal.alarm(300)
FLAG = os.environ.get("FLAG", "Alpaca{*** FAKEFLAG ***}")

chars = string.digits + string.ascii_lowercase + string.ascii_uppercase
master_key = "".join(random.choice(chars) for _ in range(16)).encode()

for _ in range(1000):
    iv = bytes.fromhex(input("iv: "))
    ciphertext = bytes.fromhex(input("ciphertext: "))
    key = master_key + iv
    plaintext = ARC4.new(key, drop=3072).decrypt(ciphertext)
    if plaintext == master_key:
        print(FLAG)
        break
    print("plaintext:", plaintext.hex())
