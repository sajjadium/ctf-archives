from random import getrandbits
from Crypto.Util.number import getPrime, long_to_bytes, bytes_to_long

def keygen(): # normal rsa key generation
  primes = []
  e = 3
  for _ in range(2):
    while True:
      p = getPrime(1024)
      if (p - 1) % 3:
        break
    primes.append(p)
  return e, primes[0] * primes[1]

def pad(m, n): # pkcs#1 v1.5
  ms = long_to_bytes(m)
  ns = long_to_bytes(n)
  if len(ms) >= len(ns) - 11:
    return -1
  padlength = len(ns) - len(ms) - 3
  ps = long_to_bytes(getrandbits(padlength * 8)).rjust(padlength, b"\x00")
  return int.from_bytes(b"\x00\x02" + ps + b"\x00" + ms, "big")

def encrypt(m, e, n): # standard rsa
  res = pad(m, n)
  if res != -1:
    print(f"c: {pow(m, e, n)}")
  else:
    print("error :(", "message too long")

menu = """
[1] enc()
[2] enc(flag)
[3] quit
"""[1:]

e, n = keygen()
print(f"e: {e}")
print(f"n: {n}")
while True:
  try:
    print(menu)
    opt = input("opt: ")
    if opt == "1":
      encrypt(int(input("msg: ")), e, n)
    elif opt == "2":
      encrypt(bytes_to_long(open("/challenge/flag.txt", "rb").read()), e, n)
    elif opt == "3":
      print("bye")
      exit(0)
    else:
      print("idk")
  except Exception as e:
    print("error :(", e)