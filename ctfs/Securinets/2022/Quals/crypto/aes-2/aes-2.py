from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os, sys, hashlib, random

FLAG = b"Securinets{REDACTED}"

key, iv1, iv2 = [os.urandom(16) for _ in range(3)]

def xor(a, b):
	return bytes(i ^ j for i, j in zip(a, b))

def get_token(msg, iv1, iv2):
	if len(msg) % 16 != 0:
		msg = pad(msg, 16)
	aes = AES.new(key, AES.MODE_ECB)
	blocks = [msg[i:i+16] for i in range(0, len(msg), 16)]
	enc = b""
	tmp1 = iv1
	tmp2 = iv2
	for block in blocks:
		tmp = aes.encrypt(xor(block, tmp1))
		_tmp = aes.encrypt(xor(tmp, tmp2))
		enc += _tmp
		tmp1 = _tmp
		tmp2 = tmp
	return enc

def proof(msg):
	res = b"\x00"*16
	for i in range(0, len(msg), 16):
		res = xor(res, msg[i:i+16])
	return hashlib.sha256(res).digest()


if __name__ == "__main__":
	alice_username = os.urandom(32)
	alice_token = get_token(alice_username, iv1, iv2)
	print(f"Alice's creds : {alice_username.hex()} -> {alice_token.hex()}\n")

	while True:
		try:
			username = bytes.fromhex(input("Username : "))
			token = get_token(username, iv1, iv2)
			print(f"Your creds : {username.hex()} -> {token.hex()}")

			if proof(token) == proof(alice_token):
				if token == alice_token:
					print(f"You are not Alice!")
					sys.exit()
				else:
					print(f"Hey Alice! Here is your flag {FLAG}")
					sys.exit()	
			else:
				print("Try again!\n")
		except Exception as e:
			print(e)
			print("Invalid input.\n")