from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes, getRandomInteger
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import numpy as np
import secrets
import hashlib
import random

FLAG = b"TRX{fake_flag_for_testing}"

# The great Roman modulus, the foundation of the Pact
p = getPrime(512)
q = getPrime(512)
n = p * q

# The public strengths of Generals Alicius and Bobius
eA = 27  # Alicius' power
eB = 35  # Bobius' power

# Secret keys, determined by fate
kA = getRandomInteger(100)
kB = kA + (-1 if random.randint(0, 1) else 1) * getRandomInteger(16)  # A slight, dangerous drift

# Alicius' secret calculations
e1 = [2, 3, 5, 7]
a1 = [69, 420, 1337, 9001]

# Bobius' secret calculations
e2 = [11, 13, 17, 19]
a2 = [72, 95, 237, 1001]

# Each general computes their part of the sacred key
c1 = sum([a * pow(kA, e, n) for a, e in zip(a1, e1)])  # Alicius' part
c2 = sum([a * pow(kB, e, n) for a, e in zip(a2, e2)])  # Bobius' part

# Encryption of each part using the other's public power
cA = pow(c1, eB, n)  # Alicius encrypts his secret for Bobius
cB = pow(c2, eA, n)  # Bobius encrypts his secret for Alicius

# The shared key, their fragile alliance
key = long_to_bytes(c1 + c2)
key = hashlib.sha256(key).digest()

# The exchange of trust
print(f"n = {n}")
print(f"eA = {eA}")
print(f"eB = {eB}")

# The encrypted secrets, waiting to be revealed
print(f"cA = {cA}")
print(f"cB = {cB}")

# The final encryption of Rome’s fate
iv = secrets.token_bytes(16)
cipher = AES.new(key, AES.MODE_CBC, iv)
ciphertext = cipher.encrypt(pad(FLAG, 16))  
print("Here is the encrypted flag") 
print(f"iv = {iv.hex()}")
print(f"ciphertext = {ciphertext.hex()}")
