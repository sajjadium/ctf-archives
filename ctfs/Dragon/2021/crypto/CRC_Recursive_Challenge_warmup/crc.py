#!/usr/bin/env python3

def crc64(buf, crc=0xffffffffffffffff):
    for val in buf:
        crc ^= val << 56
        for _ in range(8):
            crc <<= 1
            if crc & 2**64:
                crc ^= 0x1ad93d23594c935a9
    return crc

inp = input().strip().encode()
crc = crc64(inp)
if inp == f'My crc64 is 0x{crc:016x}! Cool, isn\'t it?'.encode():
    with open('flag.txt', 'r') as f:
        print(f.read().strip())
else:
    print('Nope!')
