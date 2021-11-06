import os
from Crypto.Util.number import getPrime, getRandomNBitInteger

flag = os.getenv("FLAG", "XXXX{sample_flag}").encode()
m = int.from_bytes(flag, 'big')

p = getPrime(512)
y = pow(1 + p, m, p**3)

assert m < p
print(f"p = {hex(p)}")
print(f"y = {hex(y)}")
