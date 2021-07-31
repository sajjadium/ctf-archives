#!/usr/bin/env python3

from Crypto.Util import number
from Crypto.Cipher import AES
import os, sys, random
from flag import flag

def keygen():
	iv, key = [os.urandom(16) for _ in '01']
	return iv, key

def encrypt(msg, iv, key):
	aes = AES.new(key, AES.MODE_CBC, iv)
	return aes.encrypt(msg)

def decrypt(enc, iv, key):
	aes = AES.new(key, AES.MODE_CBC, iv)
	return aes.decrypt(enc)

def die(*args):
	pr(*args)
	quit()

def pr(*args):
	s = " ".join(map(str, args))
	sys.stdout.write(s + "\n")
	sys.stdout.flush()

def sc():
	return sys.stdin.readline().strip()

def main():
	border = "+"
	pr(border*72)
	pr(border, " hi all, welcome to the simple KEYBASE cryptography task, try to    ", border)
	pr(border, " decrypt the encrypted message and get the flag as a nice prize!    ", border)
	pr(border*72)

	iv, key = keygen()
	flag_enc = encrypt(flag, iv, key).hex()

	while True:
		pr("| Options: \n|\t[G]et the encrypted flag \n|\t[T]est the encryption \n|\t[Q]uit")
		ans = sc().lower()
		if ans == 'g':
			pr("| encrypt(flag) =", flag_enc)
		elif ans == 't':
			pr("| Please send your 32 bytes message to encrypt: ")
			msg_inp = sc()
			if len(msg_inp) == 32:
				enc = encrypt(msg_inp, iv, key).hex()
				r = random.randint(0, 4)
				s = 4 - r
				mask_key = key[:-2].hex() + '*' * 4
				mask_enc = enc[:r] + '*' * 28 + enc[32-s:]
				pr("| enc =", mask_enc)
				pr("| key =", mask_key)
			else:
				die("| SEND 32 BYTES MESSAGE :X")
		elif ans == 'q':
			die("Quitting ...")
		else:
			die("Bye ...")

if __name__ == '__main__':
	main()