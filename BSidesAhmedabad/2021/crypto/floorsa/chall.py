import os
import hashlib
from Crypto.Util.number import getPrime, getRandomNBitInteger
from itertools import product

def floor_sum(n: int, m: int, a: int) -> int:
  """Fast calculation for sum([a * i // m for i in range(n)])
  """
  res, b = 0, 0
  while 0 < n:
    res += n * (n - 1) // 2 * (a // m)
    a %= m
    res += n * (b // m)
    b %= m
    last = a * n + b
    n, m, a, b = last // m, a, m, last % m
  return res

#def floor_sum_tests():
#  for n, m, a in product(range(50), range(1, 50), range(50)):
#    result = floor_sum(n, m, a) 
#    expect = sum([a * i // m for i in range(n)])
#    assert(result == expect)

if __name__ == '__main__':
  #floor_sum_tests()

  flag = os.getenv('FLAG', 'XXXX{sample_flag}').encode()
  flag += hashlib.sha512(flag).digest()
  m = int.from_bytes(flag, 'big')
  assert m.bit_length() < 2048

  p = getPrime(1024)
  q = getPrime(1024)
  n = p * q
  e = 65537
  c = pow(m, e, n)
  s = floor_sum(q, q, p)

  print(f"c = {c}")
  print(f"n = {n}")
  print(f"s = {s}")
