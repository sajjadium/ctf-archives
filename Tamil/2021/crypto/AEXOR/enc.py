from Crypto.Cipher import AES
from os import *
from binascii import *
from pwn import xor
from TamilCTF import *

key = getkey()
rep_key = getsubkey()
enc = b''
for i in range(len(key)):
	enc += hexlify(xor(key[i],rep_key[i%len(rep_key)]))

msg = flag()
iv = urandom(16)
cipher = AES.new(key,AES.MODE_XXX,iv)
ciphertext = hexlify(cipher.encrypt(msg))
print(ciphertext)
print(hexlify(iv))
print(enc)