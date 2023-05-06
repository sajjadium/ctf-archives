from Crypto.Util.number import *
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from hashlib import sha224
from random import randrange
import os

p = 148982911401264734500617017580518449923542719532318121475997727602675813514863
g = 2
assert isPrime(p//2) # safe prime

x = randrange(p)
y = pow(g, x, p)

def verify(s, e, msg):
  r_v = (pow(g, s, p) * pow(y, e, p)) % p
  return bytes_to_long(sha224(long_to_bytes(r_v) + msg).digest()) == e

def sign(msg, k):
  r = pow(g, k, p)
  e = bytes_to_long(sha224(long_to_bytes(r) + msg).digest()) % p
  s = (k - (x * e)) % (p - 1)
  return (s, e)

def xor(ba1,ba2):
  return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

otp = os.urandom(32)

messages = [
  b"Never gonna give you up",
  b"Never gonna let you down",
  b"Never gonna run around and desert you",
  b"Never gonna make you cry",
  b"Never gonna say goodbye",
  b"Never gonna tell a lie and hurt you"
]

print("p = ", p)
print("g = ", g)
print("y = ", y)

for message in messages:
  k = bytes_to_long(xor(pad(message, 32)[::-1], otp)) # OTP secure
  s, e = sign(message, k % p)
  assert (verify(s, e, message))
  print(message, sign(message, k % p))
  
flag = open("flag.txt","rb").read()
key = sha224(long_to_bytes(x)).digest()[:16]
iv = os.urandom(16)
cipher = AES.new(key, AES.MODE_CBC, iv)
ct = cipher.encrypt(pad(flag, 16)).hex()
print("ct = ", ct)
print("iv = ", iv.hex())