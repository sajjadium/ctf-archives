import random

POLY = 0xC75
FLAG_BIN_LENGTH = 360

def encode(cw):
    cw = (cw & 0xfff)
    c = cw
    for i in range(1, 12+1):
        if cw & 1 != 0:
            cw = cw ^ POLY
        cw = cw >> 1

    return (cw << 12) | c


flag = open('flag.txt', 'rb').read()

binary_str = bin(int.from_bytes(flag))[2:].zfill(FLAG_BIN_LENGTH)

blocks = [ ''.join([binary_str[12*i+j] for j in range(12)]) for i in range(FLAG_BIN_LENGTH // 12) ]
block_nos = [ int(s, 2) for s in blocks ]

encoded = [ encode(cw) for cw in block_nos ]

# flip some bits for fun
for i in range(len(encoded)):
    encoded[i] = encoded[i] ^ (1 << random.randint(0,22))
    encoded[i] = encoded[i] ^ (1 << random.randint(0,22))
    encoded[i] = encoded[i] ^ (1 << random.randint(0,22))

encoded_bin = [ bin(e)[2:].zfill(23) for e in encoded ]

print(' '.join(encoded_bin))
