from Crypto.Util.number import bytes_to_long
from Crypto.Util.number import getPrime

PRIME_LENGTH = 24
NUM_PRIMES = 256

FLAG = b"gctf{redacted}"

N = 1
e = 65537

for i in range(NUM_PRIMES):
    prime = getPrime(PRIME_LENGTH)
    N *= prime

ct = pow(bytes_to_long(FLAG), e, N)

print(f"{N=}")
print(f"{e=}")
print(f"{ct=}")
