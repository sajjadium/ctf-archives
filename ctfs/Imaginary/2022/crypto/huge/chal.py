from Crypto.Util.number import bytes_to_long, getPrime
from random import randint

flag = open("flag.txt", "rb").read()

def get_megaprime():
  primes = [getPrime(10) for _ in range(200)]
  out = 1
  for n in range(100):
    if randint(0,1) == 0:
      out *= primes[n]
  return out

p = get_megaprime()
q = get_megaprime()
n = p*q
e = 65537
m = bytes_to_long(flag)

c = pow(m, e, n)

print(f"{n = }")
print(f"{e = }")
print(f"{c = }")
