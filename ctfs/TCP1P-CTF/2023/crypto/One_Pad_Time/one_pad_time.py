import os
from pwn import xor
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

key = os.urandom(16)
iv = os.urandom(16)
cipher = AES.new(key, AES.MODE_CBC, iv)

pt = open("flag.txt", "rb").read()
ct = pad(cipher.encrypt(pt), 16)
ct = xor(ct, key)
print(f"{iv = }")
print(f"{ct = }")