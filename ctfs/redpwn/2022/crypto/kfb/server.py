#!/usr/local/bin/python -u

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from Crypto.Util.strxor import strxor
from more_itertools import ichunked

BLOCK = AES.block_size
FLAG = open('flag.txt', 'rb').read().strip()

def encrypt_block(k, pt):
  cipher = AES.new(k, AES.MODE_ECB)
  return cipher.encrypt(pt)

def encrypt(k, pt):
  assert len(k) == BLOCK
  pt = pad(pt, BLOCK)
  ct = b''
  for bk in ichunked(pt, BLOCK):
    ct += strxor(encrypt_block(k, k), bytes(bk))
  return ct

def main():
  k = get_random_bytes(BLOCK)
  enc = encrypt(k, FLAG)
  print(f'> {enc.hex()}')

  pt = bytes.fromhex(input('< '))[:BLOCK]
  enc = encrypt(k, pt)
  print(f'> {enc.hex()}')

if __name__ == '__main__':
  main()
