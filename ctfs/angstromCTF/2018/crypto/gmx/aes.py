from Crypto import Random
from Crypto.Cipher import AES

def encrypt(k, m):
	iv = Random.new().read(16)
	cipher = AES.new(k, AES.MODE_CFB, iv)
	return iv + cipher.encrypt(m)

def decrypt(k, c):
	cipher = AES.new(k, AES.MODE_CFB, c[:16])
	return cipher.decrypt(c[16:])