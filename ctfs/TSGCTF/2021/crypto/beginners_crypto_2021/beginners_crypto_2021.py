from secret import e
from Crypto.Util.number import getStrongPrime, isPrime

p = getStrongPrime(1024)
q = getStrongPrime(1024)
N = p * q
phi = (p - 1) * (q - 1)

with open('flag.txt', 'rb') as f:
    flag = int.from_bytes(f.read(), 'big')

assert(isPrime(e))
assert(isPrime(e + 2))
assert(isPrime(e + 4))

e1 = pow(e, 0x10001, phi)
e2 = pow(e + 2, 0x10001, phi)
e3 = pow(e + 4, 0x10001, phi)

c1 = pow(flag, e1, N)
c2 = pow(flag, e2, N)
c3 = pow(flag, e3, N)

print(f'p = {p}')
print(f'q = {q}')
print(f'c1 = {c1}')
print(f'c2 = {c2}')
print(f'c3 = {c3}')
