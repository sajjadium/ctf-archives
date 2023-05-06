import random
from binascii import hexlify

KEY_LEN = [REDACTED]

keybytes = []
for _ in range(KEY_LEN):
    keybytes.append(random.randrange(0,255))
print(f'key = {bytes(keybytes)}')

key = hexlify(bytes(keybytes)).decode()
with open('key.hex', 'w') as f:
    print(f'key = {key}')
    f.write(key + '\n')

