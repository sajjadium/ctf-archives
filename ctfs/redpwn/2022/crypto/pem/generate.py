from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

with open('flag.txt','rb') as f:
	flag = f.read()

key = RSA.generate(2048)
cipher_rsa = PKCS1_OAEP.new(key)
enc = cipher_rsa.encrypt(flag)

with open('privatekey.pem','wb') as f:
	f.write(key.export_key('PEM'))

with open("encrypted.bin", "wb") as f:
	f.write(enc)

