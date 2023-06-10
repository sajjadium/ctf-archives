from numba import jit, uint64, byte
from numba.pycc import CC

cc = CC('_cipher')

import numpy as np

PERM = np.array([0, 16, 32, 48, 1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35, 51, 4, 20, 36, 52, 5, 21, 37, 53, 6, 22, 38, 54, 7, 23, 39, 55, 8, 24, 40, 56, 9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59, 12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63], dtype=np.uint64)
SBOX = np.array([3, 10, 6, 8, 15, 1, 13, 4, 11, 2, 5, 0, 7, 14, 9, 12], dtype=np.uint64)
INVPERM = np.array([list(PERM).index(i) for i in range(64)], dtype=np.uint64)
INVSBOX = np.array([list(SBOX).index(i) for i in range(16)], dtype=np.uint64)
NROUNDS = 14

@cc.export('byte2int', 'uint64(byte[:])')
@jit(uint64(byte[:]))
def byte2int(blk):
    r = 0
    for i in range(8):
        r += blk[i] << (i*8)
    return r

@cc.export('int2byte', 'byte[:](uint64)')
@jit(byte[:](uint64))
def int2byte(x):
    r = np.zeros(8, dtype=np.uint8)
    for i in range(8): r[i] = (x >> (i*8))&0xff
    return r

@cc.export('toints', 'uint64[:](byte[:])')
@jit(uint64[:](byte[:]))
def toints(pt):
    r = np.zeros(len(pt)//8, dtype=np.uint64)
    for i in range(len(pt)//8): r[i] = byte2int(pt[8*i:8*i+8])
    return r

@jit(uint64(uint64))
def sub(p):
    r = 0
    for i in range(16):
        r = r | SBOX[(p >> (i*4)) & 0xf] << (i*4)
    return r

@jit(uint64(uint64))
def perm(p):
    r = 0
    for i in range(64):
        r |= ((p >> i) & 1) << PERM[i]
    return r

@cc.export('encryptblk', 'uint64(uint64, uint64[:])')
@jit(uint64(uint64, uint64[:]))
def encryptblk(p, key):
    for k in key[:-2]:
        p ^= k
        p = sub(p)
        p = perm(p)
    p ^= key[-2]
    p = sub(p)
    p ^= key[-1]
    return p

@jit(uint64(uint64))
def invsub(p):
    r = 0
    for i in range(16):
        r |= INVSBOX[(p >> (i*4)) & 0xf] << (i*4)
    return r

@jit(uint64(uint64))
def invperm(p):
    r = 0
    for i in range(64):
        r |= ((p >> i) & 1) << INVPERM[i]
    return r

@cc.export('decryptblk', 'uint64(uint64, uint64[:])')
@jit(uint64(uint64, uint64[:]))
def decryptblk(p, key):

    p ^= key[-1]
    p = invsub(p)
    p ^= key[-2]
    for k in key[:-2][::-1]:
        p = invperm(p)
        p = invsub(p)
        p ^= k
    return p

@cc.export('expandkey', 'uint64[:](uint64)')
@jit(uint64[:](uint64))
def expandkey(key):
    c = key
    ret = np.zeros(NROUNDS, dtype=np.uint64)
    for i in range(NROUNDS):
        ret[i] = c
        c *= 11704981291924017277 
        # c &= (1<<64)-1 # <-- not needed because uint64
        c = sub(c)
    return ret

@cc.export('internal_decrypt', 'byte[:](byte[:], uint64)')
@jit(byte[:](byte[:], uint64))
def internal_decrypt(pt, keyseed):
    key = expandkey(keyseed)
    ret = np.zeros(len(pt), np.uint8)
    pint = toints(pt)
    for i in range(len(pint)):
        p = pint[i]
        c = int2byte(decryptblk(p, key))
        for j in range(8): ret[8*i+j] = c[j]
    return ret

@cc.export('internal_encrypt', 'byte[:](byte[:], uint64)')
@jit(byte[:](byte[:], uint64))
def internal_encrypt(pt, keyseed):
    key = expandkey(keyseed)
    ret = np.zeros(len(pt), np.uint8)
    pint = toints(pt)
    for i in range(len(pint)):
        p = pint[i]
        c = int2byte(encryptblk(p, key))
        for j in range(8): ret[8*i+j] = c[j]
    return ret

if __name__ == "__main__":
    cc.compile()