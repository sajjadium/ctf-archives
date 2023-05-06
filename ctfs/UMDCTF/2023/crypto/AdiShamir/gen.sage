from os import urandom
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from PIL import Image
import numpy as np

p = next_prime(2^128)
F = GF(p)
R.<x> = PolynomialRing(F)

key = urandom(16)
secret = int.from_bytes(key, 'big')
k = 64
n = 128
poly = R.random_element(k-2) * x + F(secret)

px = []
for i in range(1, n+1):
	bits = list(map(np.uint8, bin(int(poly(i)))[2:].zfill(128)))
	row = [0] * 512
	for j in range(4): row[j::4] = bits
	for j in range(4): px.append(row)

im1 = Image.fromarray(np.asarray(px)*255, 'L').convert('RGBA')

with Image.open("mask.png") as im2:
	Image.alpha_composite(im1, im2).save("out.png")
	
with open("flag.png", "rb") as f, open("flag.png.enc", "wb") as g:
	cipher = AES.new(key, AES.MODE_CBC)
	g.write(cipher.iv + cipher.encrypt(pad(f.read(), 16)))