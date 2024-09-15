from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long

flag = b'ptm{REDACTED}'
flag = bytes_to_long(flag)

key = RSA.generate(2048)
n = key.n
e = key.e
p, q = key.p, key.q

leak = (p**2 + q**2 - p - q)%key.n

ciph = pow(flag, key.e, key.n)
ciph = long_to_bytes(ciph)

print(f'{n = }')
print(f'{e = }')
print(f'{ciph = }')
print(f'{leak = }')