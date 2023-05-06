from random import randrange
from Crypto.Util.number import getPrime, long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import sha256
from os import urandom

flag = open("flag.txt", "rb").read()

def und():
  p = getPrime(512)
  x = randrange(p)
  a = p ^ x ^ randrange(2**200)
  b = p ^ x ^ randrange(2**200)
  return p, a, b, x

p,a,b,x = und()

iv = urandom(16)
key = sha256(long_to_bytes(a) + long_to_bytes(b)).digest()[:16]
cipher = AES.new(key, AES.MODE_CBC, iv)

print(f"c1 = {x}")
print(f"c2 = {(x*a + b) % p}")
print(f"p = {p}")
print(f"iv = '{iv.hex()}'")
print(f"ct = '{cipher.encrypt(pad(flag, 16)).hex()}'")