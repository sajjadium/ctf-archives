#!/usr/bin/env python3
from os import urandom
from random import randint
from pwn import xor

input_img = open("flag.png", "rb").read()
outpout_img = open("flag.png.enc", "wb")

key = urandom(8) + bytes([randint(0, 9)])
outpout_img.write(xor(input_img, key))
