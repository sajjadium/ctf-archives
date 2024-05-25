from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

key = os.urandom(32)
flag = open("flag","rb").read()

while 1:
	try:
		i = bytes.fromhex(input("give input: "))
		if not i:
			break
	except:
		break
	iv = os.urandom(16)
	inp = i.replace(b"{}", flag)
	if len(inp) % 16:
		inp = pad(inp, 16)
	print(
		AES.new(key, AES.MODE_CBC, iv=iv).decrypt(inp).hex()
	)