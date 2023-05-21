from Crypto.Util.number import bytes_to_long
from secrets import randbits

FLAG = b'fake_flag'

p = randbits(1024)
q = randbits(1024)

def encrypt(msg, key):
    m = bytes_to_long(msg)
    return p * m + q * m**2 + (m + p + q) * key

n = len(FLAG)
s = randbits(1024)

print(f'n = {n}')
print(f'p = {p}')
print(f'q = {q}')
print(f'c1 = {encrypt(FLAG[:n//2], s)}')
print(f'c2 = {encrypt(FLAG[n//2:], s)}')
