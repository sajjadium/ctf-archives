from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

private_key = RSA.importKey(open('private_key.pem').read())
public_key = private_key.publickey()

def encrypt(plaintext):
	cipher_rsa = PKCS1_v1_5.new(public_key)
	ciphertext = cipher_rsa.encrypt(plaintext)
	return ciphertext

def decrypt(ciphertext):
	sentinel = b"Error in decryption!"
	try:
		cipher_rsa = PKCS1_v1_5.new(private_key)
		plaintext = cipher_rsa.decrypt(ciphertext, sentinel)
		if plaintext != b'':
			return plaintext
		else:
			raise ValueError
	except:
		return sentinel