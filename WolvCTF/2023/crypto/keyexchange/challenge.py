#!/opt/homebrew/bin/python3

from Crypto.Util.strxor import strxor
from Crypto.Util.number import *
from Crypto.Cipher import AES

n = getPrime(512)

s = getPrime(256)

a = getPrime(256)
# n can't hurt me if i don't tell you
print(pow(s, a, n))
b = int(input("b? >>> "))

secret_key = pow(pow(s, a, n), b, n)

flag = open('/flag', 'rb').read()

key = long_to_bytes(secret_key)
enc = strxor(flag + b'\x00' * (len(key) - len(flag)), key)
print(enc.hex())
