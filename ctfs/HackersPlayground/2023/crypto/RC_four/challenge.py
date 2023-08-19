from Crypto.Cipher import ARC4
from secret import key, flag
from binascii import hexlify

#RC4 encrypt function with "key" variable.
def encrypt(data):
	#check the key is long enough
	assert(len(key) > 128)

	#make RC4 instance
	cipher = ARC4.new(key)

	#We don't use the first 1024 bytes from the key stream.
	#Actually this is not important for this challenge. Just ignore.
	cipher.encrypt("0"*1024)

	#encrypt given data, and return it.
	return cipher.encrypt(data)

msg = "RC4 is a Stream Cipher, which is very simple and fast."

print (hexlify(encrypt(msg)).decode())
print (hexlify(encrypt(flag)).decode())
