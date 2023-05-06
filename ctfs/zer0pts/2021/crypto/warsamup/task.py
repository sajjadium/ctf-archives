from Crypto.Util.number import getStrongPrime, GCD
from random import randint
from flag import flag
import os

def pad(m: int, n: int):
  # PKCS#1 v1.5 maybe
  ms = m.to_bytes((m.bit_length() + 7) // 8, "big")
  ns = n.to_bytes((n.bit_length() + 7) // 8, "big")
  assert len(ms) <= len(ns) - 11

  ps = b""
  while len(ps) < len(ns) - len(ms) - 3:
    p = os.urandom(1)
    if p != b"\x00":
      ps += p
  return int.from_bytes(b"\x00\x02" + ps + b"\x00" + ms, "big")


while True:
  p = getStrongPrime(512)
  q = getStrongPrime(512)
  n = p * q
  phi = (p-1)*(q-1)
  e = 1337
  if GCD(phi, e) == 1:
    break

m = pad(int.from_bytes(flag, "big"), n)
c1 = pow(m, e, n)
c2 = pow(m // 2, e, n)

print("n =", n)
print("e =", e)
print("c1=", c1)
print("c2=", c2)
