#!/usr/bin/env python3

from Crypto.Util.number import long_to_bytes, bytes_to_long
import random
import math

def secureRand(bits, seed):
  jumbler = []
  jumbler.extend([2**n for n in range(300)])
  jumbler.extend([3**n for n in range(300)])
  jumbler.extend([4**n for n in range(300)])
  jumbler.extend([5**n for n in range(300)])
  jumbler.extend([6**n for n in range(300)])
  jumbler.extend([7**n for n in range(300)])
  jumbler.extend([8**n for n in range(300)])
  jumbler.extend([9**n for n in range(300)])
  out = ""
  state = seed % len(jumbler)
  for _ in range(bits):
    if int(str(jumbler[state])[0]) < 5:
      out += "1"
    else:
      out += "0"
    state = int("".join([str(jumbler[random.randint(0, len(jumbler)-1)])[0] for n in range(len(str(len(jumbler)))-1)]))
  return long_to_bytes(int(out, 2)).rjust(bits//8, b'\0')

def xor(var, key):
  return bytes(a ^ b for a, b in zip(var, key))

def main():
  print("Welcome to my one time pad as a service!")
  flag = open("flag.txt", "rb").read()
  seed = random.randint(0, 100000000)
  while True:
    inp = input("Enter plaintext: ").encode()
    if inp == b"FLAG":
      print("Encrypted flag:", xor(flag, secureRand(len(flag)*8, seed)).hex())
    else:
      print("Encrypted message:", xor(inp, secureRand(len(inp)*8, seed)).hex())

if __name__ == "__main__":
  main()
