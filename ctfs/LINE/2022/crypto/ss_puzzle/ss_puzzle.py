#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 64 bytes
FLAG = b'LINECTF{...}'

def xor(a:bytes, b:bytes) -> bytes:
    return bytes(i^j for i, j in zip(a, b))


S = [None]*4
R = [None]*4
Share = [None]*5

S[0] = FLAG[0:8]
S[1] = FLAG[8:16]
S[2] = FLAG[16:24]
S[3] = FLAG[24:32]

# Ideally, R should be random stream. (Not hint)
R[0] = FLAG[32:40]
R[1] = FLAG[40:48]
R[2] = FLAG[48:56]
R[3] = FLAG[56:64]

Share[0] = R[0]            + xor(R[1], S[3]) + xor(R[2], S[2]) + xor(R[3],S[1])
Share[1] = xor(R[0], S[0]) + R[1]            + xor(R[2], S[3]) + xor(R[3],S[2])
Share[2] = xor(R[0], S[1]) + xor(R[1], S[0]) + R[2]            + xor(R[3],S[3])
Share[3] = xor(R[0], S[2]) + xor(R[1], S[1]) + xor(R[2], S[0]) + R[3]
Share[4] = xor(R[0], S[3]) + xor(R[1], S[2]) + xor(R[2], S[1]) + xor(R[3],S[0])


# This share is partially broken.
Share[1] = Share[1][0:8]   + b'\x00'*8       + Share[1][16:24] + Share[1][24:32]

with open('./Share1', 'wb') as f:
    f.write(Share[1])
    f.close()

with open('./Share4', 'wb') as f:
    f.write(Share[4])
    f.close()
