import os
from Crypto.Util.number import bytes_to_long, getPrime, isPrime

flag = os.environ.get("FLAG", "fakeflag").encode()

while True:
  p = getPrime(1024)
  q = (p << 512 | p >> 512) & (2**1024 - 1) # bitwise rotation (cf. https://en.wikipedia.org/wiki/Bitwise_operation#Rotate)
  if isPrime(q): break

n = p * q
e = 0x10001
m = bytes_to_long(flag)

c = pow(m, e, n)

print(f'{n=}')
print(f'{e=}')
print(f'{c=}')
