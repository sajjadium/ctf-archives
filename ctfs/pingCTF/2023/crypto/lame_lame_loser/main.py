from hashlib import sha256
from math import gcd
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from secret import FLAG, x, y, a, b
out = open('out.txt', 'w')

assert FLAG.startswith('ping{')
assert FLAG.endswith('}')
assert x*a + y*b == 0
assert a > 0
assert b > 0
assert x.bit_length() >= 1023
assert y.bit_length() >= 1023
assert a.bit_length() == 512
assert b.bit_length() == 512
assert gcd(a, b) == 1

aes = AES.new(sha256(f'{a}||{b}'.encode()).digest(), AES.MODE_CBC, iv=bytes(16))
pt = pad(FLAG.encode(), 16)
ct = aes.encrypt(pt)

print(f'{x = }', file=out)
print(f'{y = }', file=out)
print(f'{ct = }', file=out)
