import random
from binascii import unhexlify, hexlify

KEY_LEN = [REDACTED]

with open('plaintext.txt', 'r') as f:
    pt = f.read()

with open('key.hex', 'r') as f:
    key = unhexlify(f.read().strip())

ct_bytes = []
for i in range(len(pt)):
    ct_bytes.append(ord(pt[i]) ^ key[i % KEY_LEN])

ct = bytes(ct_bytes)
print(hexlify(ct).decode() + '\n')
with open('ciphertext.txt', 'w') as f:
    f.write(hexlify(ct).decode() + '\n')

