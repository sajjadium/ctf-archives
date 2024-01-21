#!/usr/bin/env python3

from random import *
from binascii import *
from Crypto.Cipher import DES
from signal import *
import sys, os
from flag import flag

def die(*args):
	pr(*args)
	quit()

def pr(*args):
	s = " ".join(map(str, args))
	sys.stdout.write(s + "\n")
	sys.stdout.flush()

def sc():
	return sys.stdin.buffer.readline()

def shift(msg, l):
	assert l < len(msg)
	return msg[l:] + msg[:l]

def pad(text):
	if len(text) % 8 != 0:
		text += (b'\xff' * (8 - len(text) % 8))
	return text

def encrypt(msg, key):
	msg = pad(msg)
	assert len(msg) % 8 == 0
	assert len(key) == 8
	des = DES.new(key, DES.MODE_ECB)
	enc = des.encrypt(msg)
	return enc

def main():
	border = "+"
	pr(border*72)
	pr(border, ".::        Hi all, you should be fast, I mean super fact!!       ::.", border)
	pr(border, "You should send twenty 8-byte keys to encrypt the secret message and", border)
	pr(border, "just decrypt the ciphertext to get the flag, Are you ready to start?", border)
	pr(border*72)

	secret_msg = b'TOP_SECRET:' + os.urandom(40)
	
	cnt, STEP, KEYS = 0, 14, []
	md = 1

	while True:
		pr(border, "please send your key as hex: ")
		alarm(md + 1)
		ans = sc().decode().strip()
		alarm(0)
		try:
			key = unhexlify(ans)
			if len(key) == 8 and key not in KEYS:
				KEYS += [key]
				cnt += 1
			else:
				die(border, 'Kidding me!? Bye!!')
		except:
			die(border, 'Your key is not valid! Bye!!')
		if len(KEYS) == STEP:
			print(KEYS)
			HKEY = KEYS[:7]
			shuffle(HKEY)
			NKEY = KEYS[-7:]
			shuffle(NKEY)
			for h in HKEY: NKEY = [key, shift(key, 1)] + NKEY
			enc = encrypt(secret_msg, NKEY[0])
			for key in NKEY[1:]:
				enc = encrypt(enc, key)
			pr(border, f'enc = {hexlify(enc)}')
			pr(border, f'Can you guess the secret message? ')
			alarm(md + 1)
			msg = sc().strip()
			alarm(0)
			if msg == hexlify(secret_msg):
				die(border, f'Congrats, you deserve the flag: {flag}')
			else:
				die(border, f'Sorry, your input is incorrect! Bye!!')

if __name__ == '__main__':
	main()