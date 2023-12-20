from random import getrandbits as grb
from Crypto.Util.number import bytes_to_long as bl

modulus = pow(2, 32)
s_boxes = [[grb(32) for i in range(256)] for j in range(4)]
f = open("s_boxes.txt", "w")
f.write(str(s_boxes))
f.close()
initial_sub_keys = [
    "243f6a88",
    "85a308d3",
    "13198a2e",
    "03707344",
    "a4093822",
    "299f31d0",
    "082efa98",
    "ec4e6c89",
    "452821e6",
    "38d01377",
    "be5466cf",
    "34e90c6c",
    "c0ac29b7",
    "c97c50dd",
    "3f84d5b5",
    "b5470917",
    "9216d5d9",
    "8979fb1b",
]
key = "".join([hex(grb(32))[2:].zfill(8) for i in range(18)])
f = open("key.txt", "w")
f.write(str(key))
f.close()
processed_sub_keys = [
    hex(int(initial_sub_keys[i], 16) ^ int(key[8 * i : 8 * (i + 1)], 16))[2:].zfill(8)
    for i in range(len(initial_sub_keys))
]
f = open("processed_keys.txt", "w")
f.write(str(processed_sub_keys))
f.close()
pt = bin(bl(b"flag{th3_f4k3_fl4g}"))[2:]
while len(pt) % 64 != 0:
    pt = "0" + pt
pt = hex(int(pt, 2))[2:].zfill(len(pt) // 16)
ct = ""
for i in range(len(pt) // 16):
    xl = pt[16 * i : 16 * i + 8]
    xr = pt[16 * i + 8 : 16 * i + 16]
    # rounds
    for j in range(16):
        tmp = xl
        xl = bin(int(xl, 16) ^ int(processed_sub_keys[j], 16))[2:].zfill(32)
        xa = int(xl[:8], 2)
        xb = int(xl[8:16], 2)
        xc = int(xl[16:24], 2)
        xd = int(xl[24:32], 2)
        xa = (s_boxes[0][xa] + s_boxes[1][xb]) % modulus
        xc = s_boxes[2][xc] ^ xa
        f_out = (xc + s_boxes[3][xd]) % modulus
        xl = hex(int(xr, 16) ^ f_out)[2:].zfill(8)
        xr = tmp
    xrt = xr
    xr = hex(int(xl, 16) ^ int(processed_sub_keys[16], 16))[2:].zfill(8)
    xl = hex(int(xrt, 16) ^ int(processed_sub_keys[17], 16))[2:].zfill(8)
    ct += xl + xr
    f.write(str(xl) + str(xr) + "\n")
print(ct)
