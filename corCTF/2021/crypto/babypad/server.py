from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import bytes_to_long
import os

flag = open("/challenge/flag.txt").read().encode()
key = os.urandom(16)

def encrypt(pt):
  iv = os.urandom(16)
  ctr = Counter.new(128, initial_value=bytes_to_long(iv))
  cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
  return iv + cipher.encrypt(pad(pt, 16))

def decrypt(ct):
  try:
    iv = ct[:16]
    ct = ct[16:]
    ctr = Counter.new(128, initial_value=bytes_to_long(iv))
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    pt = cipher.decrypt(ct)
    unpad(pt, 16)
    return 1
  except Exception as e:
    return 0

def main():
  print(encrypt(flag).hex())
  while True:
   try:
    print(decrypt(bytes.fromhex(input("> "))))
   except Exception as e:
    pass

main()