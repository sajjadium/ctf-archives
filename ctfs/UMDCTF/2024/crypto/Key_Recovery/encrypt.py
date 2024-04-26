from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

with open("flag.txt", "rb") as f:
	flag = f.read()

with open("original.pem", "rb") as f:
	orig_key = f.read()
	key = RSA.import_key(orig_key)

cipher = PKCS1_OAEP.new(key)
ciphertext = cipher.encrypt(flag)

with open("out.txt", "wb") as f:
	f.write(ciphertext)

with open("modified.pem", "wb") as f:
	for i, line in enumerate(orig_key.splitlines()):
		f.write(line[:66-2*i] + b'\n')