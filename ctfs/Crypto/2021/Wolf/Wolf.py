#!/usr/bin/env python3

from Cryptodome.Cipher import AES
import os, time, sys, random
from flag import flag

passphrase = b'HungryTimberWolf'

def encrypt(msg, passphrase, niv):
	msg_header = 'EPOCH:' + str(int(time.time()))
	msg = msg_header + "\n" + msg + '=' * (15 - len(msg) % 16)
	aes = AES.new(passphrase, AES.MODE_GCM, nonce = niv)
	enc = aes.encrypt_and_digest(msg.encode('utf-8'))[0]
	return enc

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
	pr(border, "  hi wolf hunters, welcome to the most dangerous hunting ground!!   ", border)
	pr(border, "  decrypt the encrypted message and get the flag as a nice prize!   ", border)
	pr(border*72)

	niv = os.urandom(random.randint(1, 11))
	flag_enc = encrypt(flag, passphrase, niv)

	while True:
		pr("| Options: \n|\t[G]et the encrypted flag \n|\t[T]est the encryption \n|\t[Q]uit")
		ans = sc().lower()
		if ans == 'g':
			pr(f'| encrypt(flag) = {flag_enc.hex()}')
		elif ans == 't':
			pr("| Please send your message to encrypt: ")
			msg_inp = sc()
			enc = encrypt(msg_inp, passphrase, niv).hex()
			pr(f'| enc = {enc}')
		elif ans == 'q':
			die("Quitting ...")
		else:
			die("Bye ...")

if __name__ == '__main__':
	main()