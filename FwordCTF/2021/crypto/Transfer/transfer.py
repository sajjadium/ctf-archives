#!/usr/bin/env python3.8
from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse
from ed25519 import B, l, H, Hint, mult, add, point_to_bytes, bytes_to_point
import os, sys, hashlib, hmac, signal
                 
FLAG = "FwordCTF{###########################################################}"

WELCOME = '''
   _____                       _____
  _|   |_______________________|   |_
  |  $  |                     |  $  |
  | ||| | $$ NATIONAL BANK $$ | ||| |
  |     |                     |     |
  | [ ] |  [ ]    [ ]    [ ]  | [ ] |
  |     |---------------------|     |
  | [ ] |  _ _   .---.   _ _  | [ ] |
  |     | | | |  |_|_|  | | | |     |
  |_____|_|_|_|__|_|_|__|_|_|_|_____|
               /=======\\
'''

sk = os.urandom(32)
k = bytes_to_long(H(sk)[:32])
pk = point_to_bytes(mult(B, k))

def sign(m, sk, pk):
  m = long_to_bytes(m)
  h = H(sk)
  a = bytes_to_long(h[:32]) % l
  r = Hint(h[32:] + hmac.new(m, h, digestmod=hashlib.sha512).digest())
  R = mult(B, r)
  S = (r + Hint(point_to_bytes(R) + pk + m) * a) % l
  return point_to_bytes(R) + long_to_bytes(S)

def verify(s, m, pk):
  m = long_to_bytes(m)  
  R = bytes_to_point(s[:32])  
  A = bytes_to_point(pk)  
  S = bytes_to_long(s[32:]) 
  h = Hint(point_to_bytes(R) + pk + m) 
  r1 = mult(B, S)  
  r2 = add(R, mult(A, h)) 
  return r1 == r2


class Transfer:
    def __init__(self):
        print(WELCOME)

    def start(self):
      try:
          while True:
              print("\n1- Transfer")
              print("2- Verify")
              print("3- Leave")
              c = input("> ")

              if c == '1':
                money = int(input("\nTransfer some money to your account : "))
                assert money > 0

                if money >= 2**2048:
                    print("Sorry, I can't sign it for you.")
                else:
                    print(f"Verification code : {sign(money, sk, pk).hex()}\nPublic Key : {pk.hex()}")

              if c == '2':
                m = int(input("\nMoney : "))
                s = bytes.fromhex(input("Code : "))

                if m < 2**2048:
                    print("Transfer failed.")
                else:
                    if verify(s, m, pk):
                        print(f"Transfer Succeeded. Here is your flag : {FLAG}")
                    else:
                        sys.exit("Signature incorrect.")

              elif c == '3':
                sys.exit("Goodbye :)")

      except Exception:
          sys.exit("System error.")


signal.alarm(60)
if __name__ == "__main__":
    challenge = Transfer()
    challenge.start()