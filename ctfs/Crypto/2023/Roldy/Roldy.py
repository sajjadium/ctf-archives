#!/usr/bin/env python3

from Crypto.Util.number import *
from pyope.ope import OPE as enc
from pyope.ope import ValueRange
import sys
from secret import key, flag

def die(*args):
	pr(*args)
	quit()

def pr(*args):
	s = " ".join(map(str, args))
	sys.stdout.write(s + "\n")
	sys.stdout.flush()

def sc(): 
	return sys.stdin.buffer.readline()

def encrypt(msg, key, params):
	if len(msg) % 16 != 0:
		msg += (16 - len(msg) % 16) * b'*'
	p, k1, k2 = params
	msg = [msg[_*16:_*16 + 16] for _ in range(len(msg) // 16)]
	m = [bytes_to_long(_) for _ in msg]
	inra = ValueRange(0, 2**128)
	oura = ValueRange(k1 + 1, k2 * p + 1)
	_enc = enc(key, in_range = inra, out_range = oura)
	C = [_enc.encrypt(_) for _ in m]
	return C

def main():
	border = "|"
	pr(border*72)
	pr(border, " Welcome to Roldy combat, we implemented an encryption method to    ", border)
	pr(border, " protect our secret. Please note that there is a flaw in our method ", border)
	pr(border, " Can you examine it and get the flag?                               ", border)
	pr(border*72)

	pr(border, 'Generating parameters, please wait...')
	p, k1, k2 = [getPrime(129)] + [getPrime(64) for _ in '__']
	C = encrypt(flag, key, (p, k1, k2))

	while True:
			pr("| Options: \n|\t[E]ncrypted flag! \n|\t[T]ry encryption \n|\t[Q]uit")
			ans = sc().decode().lower().strip()
			if ans == 'e':
				pr(border, f'encrypt(flag, key, params) = {C}')
			elif ans == 't':
				pr(border, 'Please send your message to encrypt: ')
				msg = sc().rstrip(b'\n')
				if len(msg) > 64:
					pr(border, 'Your message is too long! Sorry!!')
				C = encrypt(msg, key, (p, k1, k2))
				pr(border, f'C = {C}')
			elif ans == 'q':
				die(border, "Quitting ...")
			else:
				die(border, "Bye ...")

if __name__ == '__main__':
	main()