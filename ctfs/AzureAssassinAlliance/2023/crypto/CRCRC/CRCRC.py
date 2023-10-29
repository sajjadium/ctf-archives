from base64 import *

def crc128(data, poly = 0x883ddfe55bba9af41f47bd6e0b0d8f8f):
    crc = (1 << 128) - 1
    for b in data:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ (poly & -(crc & 1))
    return crc ^ ((1 << 128) - 1)

with open('./flag.txt','r') as f:
    flag = f.readline()

YourInput = input().encode()
YourDecode = b64decode(YourInput, validate=True)

print(len(YourDecode))

assert len(YourDecode) <= 127 and YourDecode.startswith(b'Dear guest, welcome to CRCRC Magic House, If you input ') and YourDecode.endswith(b", you will get 0x9c6a11fbc0e97b1fff5844fa88b1ee2d")

YourCRC = crc128(YourInput)
print(hex(YourCRC))

if(YourCRC) == 0x9c6a11fbc0e97b1fff5844fa88b1ee2d:
    print(flag)
