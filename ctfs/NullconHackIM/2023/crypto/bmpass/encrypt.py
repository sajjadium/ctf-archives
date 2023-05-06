#!/usr/bin/env python3

from Crypto.Cipher import AES
import os, sys

img_in = open(sys.argv[1], "rb").read()
img_in += b'\00' * (16 - (len(img_in) % 16))
cipher = AES.new(os.urandom(16), AES.MODE_ECB)
img_out = cipher.encrypt(img_in)
open(sys.argv[1] + ".enc", "wb+").write(img_out)
