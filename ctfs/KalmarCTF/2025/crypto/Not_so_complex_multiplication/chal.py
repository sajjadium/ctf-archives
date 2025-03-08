
from sage.all import *

FLAG = b"kalmar{???}"

# Generate secret primes of the form x^2 + 7y^2
ps = []
x = randint(0, 2**100)
while gcd(x, 7) > 1:
    x = randint(0, 2**100)
while len(ps) < 10:
    pi = x**2 + 7*randint(0, 2**100)**2
    if is_prime(pi):
        ps.append(pi)

for p in ps:
    F = GF(p)
    E = EllipticCurve_from_j(F(int("ff", 16))**3)
    print(E.order())
print(sum(ps))

# Encrypt the flag
import hashlib
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt_flag(secret: int):
    sha1 = hashlib.sha1()
    sha1.update(str(secret).encode('ascii'))
    key = sha1.digest()[:16]
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(FLAG, 16))
    return iv.hex(), ciphertext.hex()

# Good luck! :^)
print(encrypt_flag(prod(ps)))







