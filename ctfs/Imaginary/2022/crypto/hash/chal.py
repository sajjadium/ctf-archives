#!/usr/bin/env python3

import string
import random

config = [[int(a) for a in n.strip()] for n in open("jbox.txt").readlines()] # sbox pbox jack in the box

# secure hashing algorithm 42
def sha42(s: bytes, rounds=42):
  out = [0]*21
  for round in range(rounds):
    for c in range(len(s)):
      if config[((c//21)+round)%len(config)][c%21] == 1:
        out[(c+round)%21] ^= s[c]
  return bytes(out).hex()

def main():
  print("Can you guess my passwords?")
  for trial in range(50):
    print(f"--------ROUND {trial}--------")
    password = "".join([random.choice(string.printable) for _ in range(random.randint(15,20))]).encode()
    hash = sha42(password)
    print(f"sha42(password) = {hash}")
    guess = bytes.fromhex(input("hex(password) = ").strip())
    if sha42(guess) == hash:
      print("Correct!")
    else:
      print("Incorrect. Try again next time.")
      exit(-1)
  flag = open("flag.txt", "r").read()
  print(f"Congrats! Your flag is: {flag}")

if __name__ == "__main__":
  main()
