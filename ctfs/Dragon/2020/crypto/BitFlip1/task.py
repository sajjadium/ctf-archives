#!/usr/bin/python3

from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Cipher import AES
import hashlib
import os
import base64
from gmpy2 import is_prime

FLAG = open("flag").read()
FLAG += (16 - (len(FLAG) % 16))*" "


class Rng:
  def __init__(self, seed):
    self.seed = seed
    self.generated = b""
    self.num = 0

  def more_bytes(self):
    self.generated += hashlib.sha256(self.seed).digest()
    self.seed = long_to_bytes(bytes_to_long(self.seed) + 1, 32)
    self.num += 256


  def getbits(self, num=64):
    while (self.num < num):
      self.more_bytes()
    x = bytes_to_long(self.generated)
    self.num -= num
    self.generated = b""
    if self.num > 0:
      self.generated = long_to_bytes(x >> num, self.num // 8)
    return x & ((1 << num) - 1)


class DiffieHellman:
  def gen_prime(self):
    prime = self.rng.getbits(512)
    iter = 0
    while not is_prime(prime):
      iter += 1
      prime = self.rng.getbits(512)
    print("Generated after", iter, "iterations")
    return prime

  def __init__(self, seed, prime=None):
    self.rng = Rng(seed)
    if prime is None:
      prime = self.gen_prime()

    self.prime = prime
    self.my_secret = self.rng.getbits()
    self.my_number = pow(5, self.my_secret, prime)
    self.shared = 1337

  def set_other(self, x):
    self.shared ^= pow(x, self.my_secret, self.prime)

def pad32(x):
  return (b"\x00"*32+x)[-32:]

def xor32(a, b):
  return bytes(x^y for x, y in zip(pad32(a), pad32(b)))

def bit_flip(x):
  print("bit-flip str:")
  flip_str = base64.b64decode(input().strip())
  return xor32(flip_str, x)


alice_seed = os.urandom(16)

while 1:
  alice = DiffieHellman(bit_flip(alice_seed))
  bob = DiffieHellman(os.urandom(16), alice.prime)

  alice.set_other(bob.my_number)
  print("bob number", bob.my_number)
  bob.set_other(alice.my_number)
  iv = os.urandom(16)
  print(base64.b64encode(iv).decode())
  cipher = AES.new(long_to_bytes(alice.shared, 16)[:16], AES.MODE_CBC, IV=iv)
  enc_flag = cipher.encrypt(FLAG)
  print(base64.b64encode(enc_flag).decode())
