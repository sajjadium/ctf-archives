from nacl.bindings.crypto_scalarmult import (
  crypto_scalarmult_ed25519_noclamp,
  crypto_scalarmult_ed25519_base_noclamp,
)
from nacl.bindings.crypto_core import (
  crypto_core_ed25519_scalar_mul,
  crypto_core_ed25519_scalar_reduce,
  crypto_core_ed25519_is_valid_point,
  crypto_core_ed25519_NONREDUCEDSCALARBYTES,
  crypto_core_ed25519_BYTES
)
import struct
import os
import ast
import hashlib
import random

def sha512(b):
  return hashlib.sha512(b).digest()

CONST = 4096

SECRET_LEN = int(random.randint(128, 256))
SECRET = [random.randint(1, 255) for i in range(SECRET_LEN)]

with open('flag', 'r') as f:
  FLAG = f.read()

def hsh(s):
  h = sha512(s)
  assert len(h) == crypto_core_ed25519_NONREDUCEDSCALARBYTES
  return crypto_scalarmult_ed25519_base_noclamp(crypto_core_ed25519_scalar_reduce(h))


def generate_secret_set(r):
  s = set()
  for (i, c) in enumerate(SECRET):
    s.add(hsh(bytes(str(i + 25037 * r * c).strip('L').encode('utf-8'))))
  return s


def genr():
  i = 0
  while i == 0:
    i, = struct.unpack('<I', os.urandom(4))
  return i


def handle_client1():
  print("Let's see if we share anything! You be the initiator this time.")
  r = genr()
  s = generate_secret_set(r)
  for k in range(1, CONST):
    s.add(hsh(bytes(str(k + CONST * (r % k)).strip('L').encode('utf-8'))))
  b = crypto_core_ed25519_scalar_reduce(os.urandom(crypto_core_ed25519_NONREDUCEDSCALARBYTES))
  server_s = set(crypto_scalarmult_ed25519_noclamp(b, e) for e in s)

  client_s = set()
  print("Send your data!")
  got = ast.literal_eval(input())
  for e in got:
    if not crypto_core_ed25519_is_valid_point(e):
      print("Bad client!")
      exit()

    client_s.add(e)

  server_combined_client = set(
    crypto_scalarmult_ed25519_noclamp(b, e) for e in client_s
  )

  client_resp1 = [e for e in server_combined_client]
  client_resp2 = [e for e in server_s]
  random.shuffle(client_resp1)
  random.shuffle(client_resp2)
  print(repr(client_resp1))
  print(repr(client_resp2))

  return r, s

def handle_client2(r, s):
  print("Let's see if we share anything! I'll be the initiator this time.")
  b = crypto_core_ed25519_scalar_reduce(os.urandom(crypto_core_ed25519_NONREDUCEDSCALARBYTES))
  server_s = set(crypto_scalarmult_ed25519_noclamp(b, e) for e in s)
  to_client = [e for e in server_s]
  random.shuffle(to_client)
  print(repr(to_client))

  client_s = set()
  print("Send client points: ")
  got = ast.literal_eval(input())
  for e in got:
    if not crypto_core_ed25519_is_valid_point(e):
      print("Bad client!")
      exit()

    client_s.add(e)

  masked_s = set()
  print("Send masked server points: ")
  got = ast.literal_eval(input())
  for e in got:
    if not crypto_core_ed25519_is_valid_point(e):
      print("Bad client!")
      exit()

    masked_s.add(e)

  if len(masked_s) != len(server_s):
    print("Bad client!")
    exit()

  if masked_s & server_s:
    print("Bad client!")
    exit()

  masked_c = set(crypto_scalarmult_ed25519_noclamp(b, e) for e in client_s)
  if masked_c == masked_s:
    print(FLAG)
  else:
    print("Aw, we don't share anything.")

def main():
  r, s = handle_client1()
  handle_client2(r, s)

if __name__ == "__main__":
  main()
