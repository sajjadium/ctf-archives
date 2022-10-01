import os
from Crypto.Util.number import bytes_to_long
from Crypto.Util.number import getPrime

flag = os.environ.get('FLAG', 'no flag provided...')
flag = bytes_to_long(flag.encode())

p = getPrime(1024)
q = getPrime(1024)
n = p * q
e = 65537
c = pow(flag, e, n)

print(f'n = {n}')
print(f'p = {p}')
print(f'c = {c}')
