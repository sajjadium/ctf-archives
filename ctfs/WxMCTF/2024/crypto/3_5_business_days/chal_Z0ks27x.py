import os
from Crypto.Util.number import *

ks = [bytes_to_long(os.urandom(16)) for i in range(11)]
s = [250, 116, 131, 104, 181, 251, 127, 32, 155, 191, 125, 31, 214, 151, 67, 50, 36, 123, 141, 47, 12, 112, 249, 133,
     207, 139, 161, 119, 231, 120, 136, 68, 162, 158, 110, 217, 247, 183, 176, 111, 146, 215, 159, 212, 211, 196, 209,
     137, 107, 175, 164, 128, 167, 171, 132, 237, 199, 170, 201, 228, 194, 252, 163, 172, 168, 179, 145, 221, 222, 255,
     98, 184, 150, 64, 216, 157, 187, 147, 97, 152, 148, 190, 203, 193, 62, 143, 56, 156, 153, 236, 188, 134, 230, 83,
     160, 59, 219, 76, 11, 144, 178, 254, 218, 244, 227, 96, 232, 220, 213, 165, 6, 186, 226, 239, 200, 242, 7, 154,
     180, 140, 48, 248, 135, 233, 166, 234, 192, 28, 202, 27, 24, 243, 82, 22, 185, 122, 115, 93, 13, 113, 85, 21, 52,
     55, 38, 57, 78, 66, 46, 71, 189, 195, 100, 103, 1, 72, 208, 99, 105, 74, 101, 94, 61, 240, 25, 23, 18, 84, 138, 87,
     26, 60, 204, 17, 49, 53, 169, 14, 121, 0, 79, 177, 4, 63, 241, 3, 77, 37, 2, 15, 108, 73, 118, 30, 33, 20, 54, 43,
     197, 92, 75, 95, 198, 205, 19, 142, 29, 86, 35, 109, 235, 174, 114, 210, 65, 246, 70, 80, 223, 8, 245, 182, 45, 69,
     149, 129, 90, 224, 39, 206, 130, 126, 10, 88, 91, 253, 58, 89, 81, 117, 34, 106, 124, 41, 51, 229, 40, 44, 238,
     173, 5, 9, 42, 102, 225, 16]
rots = [11, 26, 37, 49, 62, 73, 89, 104, 116]

def pad(msg, l):
    x = l-(len(msg))%l
    return msg+bytes([x]*x)

def lpad(msg, l):
    return msg+bytes(l-len(msg))

def xor(a, b):
    return bytes(i^j for i, j in zip(a,b))


def splitBlocks(pt, l):
    return [pt[l*i:l*i+l] for i in range(len(pt)//l)]


def rot(x, n):
    return ((x >> n) | (x << (128 - n))) & ((1 << 128) - 1)


def doSbox(block):
    bs = lpad(long_to_bytes(block), 16)
    return bytes_to_long(bytes([s[i] for i in bs]))


def encBlock(pt, iv):
    block = pt ^ ks[0]
    block = doSbox(block)
    for i in range(9):
        block ^= ks[i + 1]
        block ^= rot(iv, rots[i])
        block = doSbox(block)
    block ^= ks[-1]
    return block


def enc(pt):
    pt = pad(pt, 16)
    blocks = splitBlocks(pt, 16)
    iv = os.urandom(16)
    ct = iv
    for i in blocks:
        ct+=lpad(long_to_bytes(encBlock(bytes_to_long(xor(ct[-16:], i)), bytes_to_long(iv))), 16)
    return ct


flag = os.environ.get("FLAG", "wxmctf{dummy}").encode()

print(enc(flag).hex())

while True:
    inp = bytes.fromhex(input("Gimme ur plaintext block: "))
    iv = bytes.fromhex(input("Gimme ur iv: "))
    assert len(inp)==16
    assert len(iv)==16
    print(lpad(long_to_bytes(encBlock(bytes_to_long(inp), bytes_to_long(iv))), 16).hex())

