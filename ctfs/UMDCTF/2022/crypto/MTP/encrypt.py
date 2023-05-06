import random
from binascii import unhexlify, hexlify

KEY_LEN = 30

keybytes = []
for _ in range(KEY_LEN):
    keybytes.append(random.randrange(0,255))
print(f'key = {bytes(keybytes)}')

key = keybytes

with open('plaintexts.txt', 'r') as f:
    pts = f.read().strip().split('\n')

cts = []
for pt in pts:
    ct_bytes = []
    for i in range(len(pt)):
        ct_bytes.append(ord(pt[i]) ^ key[i])
    cts.append(bytes(ct_bytes))

print(' ')
with open('ciphertexts.txt', 'w') as f:
    for ct in cts:
        print(hexlify(ct).decode())
        f.write(hexlify(ct).decode() + '\n')
