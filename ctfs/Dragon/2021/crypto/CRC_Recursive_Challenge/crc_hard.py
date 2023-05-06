#!/usr/bin/env python3

def crc128(buf, crc=0xffffffffffffffffffffffffffffffff):
    for val in buf:
        crc ^= val << 120
        for _ in range(8):
            crc <<= 1
            if crc & 2**128:
                crc ^= 0x14caa61b0d7fe5fa54189d46709eaba2d
    return crc

inp = input().strip().encode()
crc = crc128(inp)
if inp == f'My crc128 is 0x{crc:032x}! Cool, isn\'t it?'.encode():
    with open('flag.txt', 'r') as f:
        print(f.read().strip())
else:
    print('Nope!')
