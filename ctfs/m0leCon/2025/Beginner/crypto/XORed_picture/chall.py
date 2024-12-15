from pwn import xor
from os import urandom

key = urandom(16)

fin = open("flag.png", "rb")
fout = open("flag_enc.png", "wb")

pt = fin.read()
ct = xor(pt, key)

fout.write(ct)

fin.close()
fout.close()