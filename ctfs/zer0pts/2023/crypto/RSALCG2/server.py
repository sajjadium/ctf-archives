import os
import random
import signal
import dataclasses

from Crypto.Hash import SHA256
from Crypto.Util.number import getPrime, getRandomInteger

FLAG = os.getenv("FLAG", "zer0pts{*** REDACTED ***}")
# no seed cracking!
SEED = SHA256.new(FLAG.encode()).digest()
while len(SEED) < 623 * 4:
  SEED += SHA256.new(SEED).digest()
random.seed(SEED)

def deterministicGetPrime(bits):
  return getPrime(bits, randfunc=random.randbytes)

def deterministicGetRandomInteger(bits):
  return getRandomInteger(bits, randfunc=random.randbytes)

@dataclasses.dataclass
class RSALCG:
  a: int
  b: int
  e: int
  n: int
  s: int
  def next(self):
    self.s = (self.a * self.s + self.b) % self.n
    return pow(self.s, e, n)

def decrypt(rands, msg):
  assert len(msg) <= 128
  m = int.from_bytes(msg, "big")
  for rand in rands:
    res = rand.next()
    m ^= res
    print(f"debug: {m}")
    m ^= rand.s
  return m.to_bytes(128, "big")

ROUND = 30

a = deterministicGetRandomInteger(1024)
b = deterministicGetRandomInteger(1024)
e = 65535
n = deterministicGetPrime(512) * deterministicGetPrime(512)
print(f"{a = }")
print(f"{b = }")
print(f"{e = }")
print(f"{n = }")

# ATTENTION: s is NOT deterministic!
rands = [RSALCG(a, b, e, n, getRandomInteger(1024) % n) for _ in range(ROUND)]

signal.alarm(150)

while True:
  m = decrypt(rands, bytes.fromhex(input("> ")))
  if m.lstrip(b"\x00") == b"Give me the flag!":
    print(f"Sure! The flag is: {FLAG}")
    break
  
  print("I couldn't understand what you meant...")
