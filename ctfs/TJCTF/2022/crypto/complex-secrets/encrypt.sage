from sage.geometry.hyperbolic_space.hyperbolic_isometry import moebius_transform

from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

CC = ComplexField(1000)
M = random_matrix(CC, 2, 2)
f = lambda z: moebius_transform(M, z)

for _ in range(3):
  z = CC.random_element()
  print(f'{z}, {f(z)}')

kz = CC.random_element()
print(kz)
kw = f(kz)

mod = 2^128
key = (kw.real() * mod).round() % mod
iv = (kw.imag() * mod).round() % mod

cipher = AES.new(long_to_bytes(key), AES.MODE_CBC, iv=long_to_bytes(iv))
flag = open('flag.txt', 'rb').read().strip()
print(cipher.encrypt(pad(flag, AES.block_size)).hex())
