import random

with open('flag.txt', 'rb') as f:
    plaintext = f.read()

key = random.randrange(256)
ciphertext = [key ^ byte for byte in plaintext]

with open('output.txt', 'w') as f:
    f.write(bytes(ciphertext).hex())
