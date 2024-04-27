#!/usr/local/bin/python
from os import urandom
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

key = bytes.fromhex(open("key.txt", "r").read())
keys = [key[i:i+8] for i in range(0, len(key), 8)]
flag = open("flag.txt", "rb").read()

enc = pad(flag, 8)
for i in range(3):
	cipher = DES.new(keys[i], DES.MODE_CBC)
	enc = cipher.iv + cipher.encrypt(enc)
print("Here's the encrypted flag:", enc.hex())

while 1:
	print("Give us an encrypted text and we'll tell you if it's valid!")
	enc = input()
	try: enc = bytes.fromhex(enc)
	except:
		print("no")
		break
	if len(enc) % 8 != 0 or len(enc) < 32:
		print("no")
		break
	try:
		for i in range(3):
			iv, enc = enc[:8], enc[8:]
			cipher = DES.new(keys[2-i], DES.MODE_CBC, iv=iv)
			enc = cipher.decrypt(enc)
		dec = unpad(enc, 8)
		print("yes")
	except:
		print("no")
