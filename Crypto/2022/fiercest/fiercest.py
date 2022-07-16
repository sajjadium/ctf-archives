#!/usr/bin/env python3

from Crypto.Util.number import *
import sys
from flag import flag

def diff(a, b):
	assert a.bit_length() == b.bit_length()
	w, l = 0, a.bit_length()
	for _ in range(l):
		if bin(a)[2:][_] != bin(b)[2:][_]: w += 1
	return w

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
	pr(border, "Hello guys! This is a challenge on fault attack for signatures, our ", border)
	pr(border, "storage can apply at most `l' bit flip-flop on signature modulus, so", border)
	pr(border, "try to locate the critical bits, we'll changed them to forge a sign!", border)
	pr(border*72)

	nbit = 512
	p, q = [getPrime(nbit) for _ in '__']
	n, e = p * q, 65537
	B, l = [int(b) for b in bin(n)[2:]], 2
	
	MSG = "4lL crypt0sy5t3ms suck5 fr0m faul7 atTaCk5 :P"
	m = bytes_to_long(MSG.encode('utf-8'))

	while True:
		pr("| Options: \n|\t[A]pply fault \n|\t[G]et the parameters \n|\t[V]erify the signature \n|\t[Q]uit")
		ans = sc().lower()
		if ans == 'a':
			_B = B
			pr(border, f"please send at most {l}-tuple array from indices of bits of modulus, like: 14, 313")
			ar = sc()
			try:
				ar = [int(_) for _ in ar.split(',')]
				if len(ar) <= l:
					for i in range(len(ar)): _B[ar[i]] = (_B[ar[i]] + 1) % 2
					N = int(''.join([str(b) for b in _B]), 2)
				else: raise Exception('Invalid length!')
			except: pr(border, "Something went wrong!!")
		elif ans == 'g':
			pr(border, f'e = {e}')
			pr(border, f'n = {n}')
		elif ans == "v":
			pr(border, "please send signature to verify: ")
			_flag, signature = False, sc()
			try:
				signature = int(signature)
				if pow(signature, e, N) == m: _flag = True
				else: pr(border, "Your signature is not valid!!")
			except:
				pr(border, "Something went wrong!!")
			if _flag: die(border, "Congrats! your got the flag: " + flag)
		elif ans == 'q': die("Quitting ...")
		else: die("Bye bye ...")

if __name__ == "__main__": main()