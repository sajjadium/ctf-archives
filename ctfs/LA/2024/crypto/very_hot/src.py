from Crypto.Util.number import getPrime, isPrime, bytes_to_long
from flag import FLAG

FLAG = bytes_to_long(FLAG.encode())

p = getPrime(384)
while(not isPrime(p + 6) or not isPrime(p + 12)):
    p = getPrime(384)
q = p + 6
r = p + 12

n = p * q * r
e = 2**16 + 1
ct = pow(FLAG, e, n)

print(f'n: {n}')
print(f'e: {e}')
print(f'ct: {ct}')

