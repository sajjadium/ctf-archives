from Crypto.Util.number import getStrongPrime

# We get 2 1024-bit primes
p = getStrongPrime(1024)
q = getStrongPrime(1024)

# We calculate the modulus
n = p*q

# We generate our encryption key
import secrets
e = secrets.randbelow(n)

# We take our input
flag = b"irisctf{REDACTED_REDACTED_REDACTED}"
assert len(flag) == 35
# and convert it to a number
flag = int.from_bytes(flag, byteorder='big')

# We encrypt our input
encrypted = (flag * e) % n

print(f"n: {n}")
print(f"e: {e}")
print(f"flag: {encrypted}")
