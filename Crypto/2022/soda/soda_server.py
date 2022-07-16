#!/usr/bin/env python3

from Crypto.Util.number import *
import sys
from secret import p, q, flag

def soda(g, p, q, m):
	n, phi = p * q, (p - 1) * (q - 1)
	if isPrime(m) and m.bit_length() <= 128:
		e = m
	else:
		e = 2 * (pow(g, m**2, n) % 2**152) ^ 1
	if GCD(e, phi) == 1:
		d = inverse(e, phi)
		return pow(g, d, n)

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
	pr(border, "Hi all cryptographers! Welcome to SODA crypto oracle, we do SODAing!", border)
	pr(border, "You mission is find a way to SODA a given message, I think its easy.", border)
	border = "|"
	
	n = p * q
	phi = (p - 1) * (q - 1)
	g = 31337

	CRY = "Long Live Crypto :))"
	m = bytes_to_long(CRY.encode('utf-8'))

	while True:
		pr("| Options: \n|\t[G]et the parameters \n|\t[T]ry the soda \n|\t[V]erify the signature \n|\t[Q]uit")
		ans = sc().lower()

		if ans == 'g':
			pr(border, f'n = {n}')
			pr(border, f'g = {g}')
		elif ans == 't':
			pr(border, "please send your integer to get soda: ")
			s = sc()
			try:
				s = int(s)
			except:
				die(border, "Something went wrong! Your input is not valid!! Bye!!!")
			h = soda(g, p, q, s)
			if h != None:
				if s == m:
					die(border, 'Are you kidding me? We will never SODA it!! Bye!!!')
				else:
					pr(border, f"soda(g, p, q, m) = {soda(g, p, q, s)}")
			else:
				pr(border, 'Something went wrong! See source code!!')	
		elif ans == "v":
			pr(border, "please send the soda to verify: ")
			sd = sc()
			try:
				sd = int(sd)
			except:
				die(border, "Your input is not valid! Bye!!")
			_e = 2 * (pow(g, m**2, n) % 2**152) ^ 1
			if pow(sd, _e, n) == g:
				die(border, "Congrats! your got the flag: " + flag)
			else:
				pr(border, "[ERR]: Your answer is NOT correct!!!")
		elif ans == 'q':
			die(border, "Quitting ...")
		else:
			die(border, "Bye bye ...")

if __name__ == "__main__":
	main()