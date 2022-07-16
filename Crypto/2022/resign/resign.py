#!/usr/bin/env python3

from Crypto.Util.number import *
from hashlib import sha1
import sys
from flag import flag

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
	border = "|"
	pr(border*72)
	pr(border, " Hi, Try to guess our RSA private key to sign my message, talented  ", border)
	pr(border, " hackers like you ;) are able to do it, they are *Super Guesser* :) ", border)
	pr(border*72)

	p, q = [getPrime(1024) for _ in '__']
	n, e = p * q, 65537
	phi = (p - 1) * (q - 1)
	d = inverse(e, phi)

	MSG = b'::. Can you forge any signature? .::'
	h = bytes_to_long(sha1(MSG).digest())
	SIGN = pow(h, d, n)

	while True:
		pr("| Options: \n|\t[G]uess the secret key \n|\t[R]eveal the parameters \n|\t[S]ign the message \n|\t[P]rint the signature \n|\t[Q]uit")
		ans = sc().lower()
		if ans == 'g':
			pr(border, f"please send the RSA public exponent and PARAMS p, q separated by comma like e, p, q: ")
			PARAMS = sc()
			try:
				E, P, Q = [int(_) for _ in PARAMS.split(',')]
				if P.bit_length() == Q.bit_length() == 1024 and P != Q:
					N = P * Q
					PHI = (P - 1) * (Q - 1)
					D = inverse(E, PHI)
					if pow(h, D, N) == SIGN:
						e, n, d = E, N, D
						pr(border, 'Great guess, now you are able to sign any message!!!')
					else:
						pr(border, 'Your RSA parameters are not correct!!')
				else: raise Exception('Invalid RSA parameters!!')
			except: pr(border, "Something went wrong!!")
		elif ans == 'r':
			pr(border, f'e = {e}')
			pr(border, f'n = {n}')
		elif ans == "p":
			pr(border, f'SIGN = {SIGN}')
		elif ans == 's':
			pr(border, "Please send the signature of this message: ")
			pr(border, f"MSG = {MSG[4:-4]}")
			sgn = sc()
			try:
				sgn = int(sgn)
				_continue = True
			except:
				pr(border, "Something went wrong!!")
				_continue = False
			if _continue:
				_MSG = MSG[4:-4]
				_h = bytes_to_long(sha1(_MSG).digest())
				if pow(sgn, e, n) == _h:
					die(border, "Congrats! your got the flag: " + flag)
				else: 
					pr(border, "Sorry, your signature is not correct!")
		elif ans == 'q': die("Quitting ...")
		else: die("Bye bye ...")

if __name__ == "__main__": main()