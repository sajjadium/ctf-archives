#!/usr/bin/env python3

from Crypto.Util.number import *
import sys
from secret import privkey, flag

def encrypt(m, pubkey):
	g, n = pubkey
	c = pow(g, m, n ** 2)
	return c

def main():
	border = "|"
	pr(border*72)
	pr(border, " Welcome to Quremo battle, try our ultra secure encryption oracle!  ", border)
	pr(border, " You can change the base of encryption schema by given circumstance!", border)
	pr(border*72)
	nbit = 128
	p, q = privkey
	g, n = 5, p * q
	pkey = (g, n)
	_flag = bytes_to_long(flag.lstrip(b'flag{').rstrip(b'}'))
	while True:
		pr("| Options: \n|\t[E]ncrypted flag! \n|\t[P]ublic key \n|\t[T]ry encryption with your desired g \n|\t[Q]uit")
		ans = sc().lower()
		if ans == 'e':
			enc = encrypt(_flag, pkey)
			pr(border, f'encrypt(flag, pkey) = {enc}')
		elif ans == 't':
			pr(border, "Send the parameters g: ")
			_g = sc()
			try: _g = int(_g)
			except:
				die(border, "your parameter is not integer!")
			if pow(n, 2, _g) * isPrime(_g) == 1:
				pkey = (_g, n)
				enc = encrypt(_flag, pkey)
				pr(border, f'enc = {enc}')
			else:
				die(border, "g is not valid :(")
		elif ans == 'p':
			pr(border, f'pubkey = {pkey}')
		elif ans == 'q':
			die(border, "Quitting ...")
		else:
			die(border, "Bye ...")

def die(*args):
	pr(*args)
	quit()

def pr(*args):
	s = " ".join(map(str, args))
	sys.stdout.write(s + "\n")
	sys.stdout.flush()

def sc():
	return sys.stdin.readline().strip()

if __name__ == '__main__':
	main()