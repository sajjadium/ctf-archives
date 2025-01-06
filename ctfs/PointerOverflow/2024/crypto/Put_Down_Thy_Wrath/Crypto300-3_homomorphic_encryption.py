# homomorphic_encryption.py

import random
import binascii

class FlawedHomomorphicEncryption:
    def __init__(self, p, q):
        self.n = p * q
        self.p = p
        self.q = q
        self.public_key = self.n

    def encrypt(self, message):
        encrypted_message = []
        for char in message:
            m = ord(char)
            r = random.randint(1, self.n - 1)
            c = (m * r) % self.n
            encrypted_message.append(c)
        return encrypted_message

    def decrypt(self, encrypted_message):
        decrypted_message = []
        for c in encrypted_message:
            m = (c * pow(r, -1, self.n)) % self.n
            decrypted_message.append(chr(m))
        return ''.join(decrypted_message)

# Parameters (small primes for illustration; not secure)
p = 61
q = 53

# Create encryption object
encryption = FlawedHomomorphicEncryption(p, q)

# Flag message to encrypt
flag = "poctf{uwsp_T3mp357_4nd_7urnm01l}"

# Encrypt the flag
encrypted_message = encryption.encrypt(flag)

# Save public key and encrypted message
public_key = encryption.public_key
encrypted_message_hex = [binascii.hexlify(bytes([c])).decode() for c in encrypted_message]

with open("public_key.txt", "w") as pub_file:
    pub_file.write(str(public_key))

with open("encrypted_message.txt", "w") as enc_file:
    enc_file.write(','.join(encrypted_message_hex))

print(f"Generated homomorphic encryption and encrypted message.")
print(f"Public key saved to 'public_key.txt'.")
print(f"Encrypted message saved to 'encrypted_message.txt'.")
