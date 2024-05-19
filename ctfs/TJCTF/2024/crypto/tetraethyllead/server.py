#!/usr/local/bin/python3 -u

import secrets
import hashlib
from Crypto.Util.number import bytes_to_long, long_to_bytes

def rrot(word, i):
    i %= 32
    word = word & ((1 << 32) - 1)
    return ((word >> i) | (word << (32 - i))) & ((1 << 32) - 1)

def lrot(word, i):
    i %= 32
    word = word & ((1 << 32) - 1)
    return ((word << i) | (word >> (32 - i))) & ((1 << 32) - 1)
    

def get_sbox(word):
    
    Sbox = [17, 16, 19, 18, 21, 20, 23, 22, 25, 24, 27, 26, 29, 28, 31, 30, 1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14, 49, 48, 51, 50, 53, 52, 55, 54, 57, 56, 59, 58, 61, 60, 63, 62, 33, 32, 35, 34, 37, 36, 39, 38, 41, 40, 43, 42, 45, 44, 47, 46, 81, 80, 83, 82, 85, 84, 87, 86, 89, 88, 91, 90, 93, 92, 95, 94, 65, 64, 67, 66, 69, 68, 71, 70, 73, 72, 75, 74, 77, 76, 79, 78, 113, 112, 115, 114, 117, 116, 119, 118, 121, 120, 123, 122, 125, 124, 127, 126, 97, 96, 99, 98, 101, 100, 103, 102, 105, 104, 107, 106, 109, 108, 111, 110, 145, 144, 147, 146, 149, 148, 151, 150, 153, 152, 155, 154, 157, 156, 159, 158, 129, 128, 131, 130, 133, 132, 135, 134, 137, 136, 139, 138, 141, 140, 143, 142, 177, 176, 179, 178, 181, 180, 183, 182, 185, 184, 187, 186, 189, 188, 191, 190, 161, 160, 163, 162, 165, 164, 167, 166, 169, 168, 171, 170, 173, 172, 175, 174, 209, 208, 211, 210, 213, 212, 215, 214, 217, 216, 219, 218, 221, 220, 223, 222, 193, 192, 195, 194, 197, 196, 199, 198, 201, 200, 203, 202, 205, 204, 207, 206, 241, 240, 243, 242, 245, 244, 247, 246, 249, 248, 251, 250, 253, 252, 255, 254, 225, 224, 227, 226, 229, 228, 231, 230, 233, 232, 235, 234, 237, 236, 239, 238]

    words = [hashlib.sha256(word).digest()]
    
    for i in range(7):
        words.append(hashlib.sha256(words[i]).digest())
        
    words = b"".join(words)

    for idx in range(0, len(words), 2):
        a = words[idx]
        b = words[idx + 1]
        old = Sbox[a]
        Sbox[a] = Sbox[b]
        Sbox[b] = old
        
    return Sbox

def getbit(byte, i):
    return (byte >> i) & 1

def setbit(v, i):
    return v << i
    
def pbox(byte):
    out = 0
    pos_subs = [4, 1, 0, 6, 3, 5, 7, 2]
    for pos_in in range(8):
        out |= setbit(getbit(byte, pos_in), pos_subs[pos_in])
    return out

def pad1(b):
    while len(b) != 1:
        b = b"\x00" + b
    return b

def r1(i, box):
    out = []

    i = long_to_bytes(i)

    for byte in i:
        out.append(box[byte])

    for idx in range(1, len(out)):
        out[idx] ^= out[idx - 1]

    return  bytes_to_long(b"".join([pad1(long_to_bytes(l)) for l in out]))


def r2(i, box):
    out = []

    i = long_to_bytes(i)

    for byte in i:
        out.append(box[byte])
        
    for idx in range(len(out) - 2, -1, -1):
        out[idx] ^= out[idx + 1]

    return bytes_to_long(b"".join([long_to_bytes(l) for l in out]))

def zpad(i):
    while len(i) != 4:
        i = b"\x00" + i
    return i

def zpad8(i):
    while len(i) < 8:
        i = b"\x00" + i
    return i

def r345(word, k, rnum):
    word ^= rrot(word, -463 + 439 * rnum + -144 * rnum**2 + 20 * rnum**3 - rnum**4) ^ lrot(word, 63 + -43 * rnum + 12 * rnum**2 + -rnum**3)

    word = (4124669716 + word * bytes_to_long(k))**3

    word ^= word << 5
    word ^= word << 5

    word ^= rrot(word, -463 + 439 * rnum + -144 * rnum**2 + 20 * rnum**3 - rnum**4) ^ lrot(word, 63 + -43 * rnum + 12 * rnum**2 + -rnum**3)


    return rrot(word, -504 + 418 * rnum -499 * rnum**2 + -511 * rnum**3 + 98 * rnum**4) & 0xffffffff

def swap(l, r):
    return r, l

def encrypt(i, k, p = False):

    k1 = k[:4]
    k2 = k[4:]

    assert len(k) == 8
    assert len(i) == 8

    m_sbox_1 = get_sbox(k1)
    m_sbox_2 = get_sbox(k2)

    l = bytes_to_long(i[:4])
    r = bytes_to_long(i[4:])
    if (p):
        print("R0:",l, r)
    #round 1
    l ^= r2(r, m_sbox_2) 
    l, r = swap(l,r)
    if (p):
        print("R1:",l, r)
    #round 2
    l ^= r1(r, m_sbox_1)
    l, r = swap(l,r)
    if (p):
        print("R2:",l, r)

    #round 3
    l ^= r345(r, k1, 3)
    l, r = swap(l,r)
    if (p):
        print("R3:",l, r)
    #round 4
    l ^= r345(r, k2, 4)
    l, r = swap(l,r)
    if (p):
        print("R4:",l, r)

    #round 5
    l ^= r345(r, long_to_bytes(bytes_to_long(k2) ^ bytes_to_long(k1)), 5)
    l, r = swap(l,r)
    if (p):
        print("R5:",l, r)

    #round 6
    l ^= r345(r, k1, 6)
    l, r = swap(l,r)
    if (p):
        print("R6:",l, r)

    #round 7
    l ^= r345(r, k2, 7)
    r ^= l
    if (p):
        print("R7:",l, r)

        
    
    return long_to_bytes((l << 32) | r)


# I want you to be happy
seecrit = b"\x00" + secrets.token_bytes(7)

for i in range(1024):
    p = int(input("p: "))
    print(bytes_to_long(encrypt(zpad8(long_to_bytes(p)), seecrit)))

guess = int(input("k: "))
if (guess == bytes_to_long(seecrit)):
    print(open("flag.txt","r").read())
