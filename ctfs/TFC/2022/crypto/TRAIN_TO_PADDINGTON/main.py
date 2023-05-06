import os

BLOCK_SIZE = 16
FLAG = b'|||REDACTED|||'


def pad_pt(pt):
    amount_padding = 16 if (16 - len(pt) % 16) == 0 else 16 - len(pt) % 16
    return pt + (b'\x3f' * amount_padding)


pt = pad_pt(FLAG)
key = os.urandom(BLOCK_SIZE)

ct = b''

j = 0
for i in range(len(pt)):
    ct += (key[j] ^ pt[i]).to_bytes(1, 'big')
    j += 1
    j %= 16

with open('output.txt', 'w') as f:
    f.write(ct.hex())