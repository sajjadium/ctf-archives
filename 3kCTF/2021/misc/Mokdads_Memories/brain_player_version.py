#!/usr/bin/python3

from PIL import Image
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Cipher import AES

mok = Image.open("el_mok.png")
mok_bytes = mok.tobytes()
iv = (X, X, X, X, X, X, X, X) # Of course it's REDACTED
prev = iv
fmok_pixels = []

for i in range(0, len(mok_bytes), 8):
    prev = tuple(map(lambda x, y: x ^ y, mok_bytes[i:i+8], prev))
    fmok_pixels.append(prev)

fmok_bytes = b"".join(map(bytearray, fmok_pixels))
k = (int("".join([hex(_)[2:] for _ in iv]), 16) ** 4).to_bytes(32, "little") # b'\x10\x82u\x98:\x1c\x0fy\x10/4{\xd8\xc3\xa9u\xe3x\x8a\x9d3ru\xc1\x93\xf5i\x8c6\xdf\x15\x01'
iv = b'\xbb\x9c\xe2\x8d\xd0\xd1\xbe@\xf6l\x02\xc95\x15\x1cF'
aes = AES.new(k, AES.MODE_CBC, iv)
ffmok_bytes = aes.encrypt(fmok_bytes[:-4]) + fmok_bytes[-4:]
key = bytes_to_long(b"REDACTED") # Mekdad will give you the key
fffmok_pixels = []

for i in range(0, len(ffmok_bytes) - 4, 8):
    p = bytes_to_long(ffmok_bytes[i:i+8])
    v = (key ^ p) % 18446744073709551615
    o2 = v & 0xff
    b2 = (v >> 8) & 0xff
    g2 = (v >> 16) & 0xff
    r2 = (v >> 24) & 0xff
    o1 = (v >> 32) & 0xff
    b1 = (v >> 40) & 0xff
    g1 = (v >> 48) & 0xff
    r1 = (v >> 56) & 0xff
    fffmok_pixels.append((r1, g1, b1, o1))
    fffmok_pixels.append((r2, g2, b2, o2))

fffmok_pixels.append(tuple(ffmok_bytes[-4:]))
fffmok = Image.new("RGBA", (887, 499))
pixels = fffmok.load()
itr = 0

for y in range(887): # Brain of Mekdad is so old not knowing how to save his memories :-(
    for x in range(499):
        pixels[y, x] = fffmok_pixels[itr]
        itr += 1

fffmok.save("brain_memory.png")