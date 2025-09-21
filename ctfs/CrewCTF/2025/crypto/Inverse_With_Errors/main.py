import secrets
import hashlib

from Crypto.Cipher import AES
from Crypto.Util.number import getPrime
from Crypto.Util.Padding import pad


flag = b'crew{*** REDACTED ***}'

N_size = 1024

N = secrets.randbits(N_size) | (1 << N_size)
d = N

while d >= N:
    d = getPrime(N_size)

values = []
R = []

for _ in range(30):
    r = secrets.randbits(100)
    R.append(r)
    values.append(pow(d, -1, N + r))

key = hashlib.sha256(str(d).encode()).digest()
flag = pad(flag, 16)

cipher = AES.new(key, AES.MODE_CBC)
iv = cipher.iv.hex()
enc = cipher.encrypt(flag).hex()

print(f'{R = }')
print(f'{values = }')
print(f'{iv = }')
print(f'{enc = }')
