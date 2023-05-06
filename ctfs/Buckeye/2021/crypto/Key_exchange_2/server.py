import random
import hashlib

# Mac/Linux: pip3 install pycryptodome
# Windows: py -m pip install pycryptodome
import Crypto.Util.number as cun
from Crypto.Cipher import AES

rand = random.SystemRandom()
FLAG = b"buckeye{???????????????????????????????????????}"


def diffie_hellman(message: bytes):
    p = cun.getPrime(512)
    g = 5
    print(f"p = {p}")
    print(f"g = {g}")

    a = rand.randrange(2, p - 1)  # private key
    A = pow(g, a, p)  # public key

    print("Can you still get the shared secret without my public key A?")

    B = int(input("Give me your public key B: "))
    if not (1 < B < p - 1):
        print("Suspicious public key")
        return

    # B ^ a === (g ^ b) ^ a === g ^ (ab)  (mod p)
    # Nobody can derive this shared secret except us!
    shared_secret = pow(B, a, p)

    # Use AES, a symmetric cipher, to encrypt the flag using the shared key
    key = hashlib.sha1(cun.long_to_bytes(shared_secret)).digest()[:16]
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(message)
    print(f"ciphertext = {ciphertext.hex()}")


print("I'm going to send you the flag.")
print("However, I noticed that an FBI agent has been eavesdropping on my messages,")
print("so I'm going to send it to you in a way that ONLY YOU can decrypt the flag.")
print()
diffie_hellman(FLAG)
