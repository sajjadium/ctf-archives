#!/usr/bin/env python3
from Crypto.Cipher import DES
import random


def splitn(text, size):
	return [text[i:i+size] for i in range(0,len(text),size)]

def encrypt(m, key):
	cipher = DES.new(key, DES.MODE_ECB)
	return cipher.encrypt(m)


flag = open('flag.png','rb').read()
ff = splitn(flag, 8)

assert len(flag) % 8 == 0, len(flag)

key = random.randbytes(8)
enc_flag = encrypt(flag, key)

random.seed(ff[0])
random.shuffle(ff)

ff = b''.join(ff)
enc_ff = encrypt(ff, key)

open('flag.png.enc', 'wb').write(enc_flag)
open('ff_error.png', 'wb').write(ff)
open('ff_error.png.enc', 'wb').write(enc_ff)
