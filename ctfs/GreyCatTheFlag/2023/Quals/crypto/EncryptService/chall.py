import os 
from Crypto.Cipher import AES 
from hashlib import sha256 

FLAG = "grey{fake_flag_please_change_this}"
assert(len(FLAG) == 40)

secret_key = os.urandom(16)

def encrypt(plaintext, iv):
    hsh = sha256(iv).digest()[:8]
    cipher = AES.new(secret_key, AES.MODE_CTR, nonce=hsh)
    ciphertext = cipher.encrypt(plaintext)
    return ciphertext.hex()

print("AES is super safe. You have no way to guess my key anyways!!")
print("My encryption service is very generous. Indeed, so generous that we will encrypt any plaintext you desire many times")

try:
    plaintext = bytes.fromhex(input("Enter some plaintext (in hex format): "))
except ValueError:
    print("We are incredibly generous, yet you display such selfishness by failing to provide a proper hex string")
    exit(0)

for i in range(256):
    ciphertext = encrypt(plaintext, i.to_bytes(1, 'big'))
    print(f"Ciphertext {i}: {ciphertext}")

print()
print("We will reward a lot of money for the person that can decipher this encrypted message :)")
print("It's impossible to decipher anyways, but here you go: ")
print("Flag: ", encrypt(FLAG.encode("ascii"), os.urandom(1)))