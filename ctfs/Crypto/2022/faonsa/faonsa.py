#!/usr/bin/env python3

from Crypto.Util.number import *
from math import gcd
import sys
from flag import flag

def diff(a, b):
	assert a.bit_length() == b.bit_length()
	w, l = 0, a.bit_length()
	for _ in range(l):
		if bin(a)[2:][_] != bin(b)[2:][_]: w += 1
	return w

def sign_esa(pubkey, x, m):
	g, p, y = pubkey
	while True:
		k = getRandomRange(2, p-1)
		if gcd(k, p-1) == 1:
			break
	u = pow(g, k, p)
	v = (m - x * u) * inverse(k, p - 1) % (p - 1)
	return (u, v)

def verify_esa(pubkey, sgn, m):
	g, p, y = pubkey
	u, v = sgn
	return pow(y, u, p) * pow(u, v, p) % p == pow(g, m, p)

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
	pr(border, "Hello guys! This is a another challenge on fault attack too, again  ", border)
	pr(border, "our storage could apply at most `l' bit fault on ElGamal modulus, p,", border)
	pr(border, "try to sign the given message and get the flag! Have fun and enjoy!!", border)
	pr(border*72)
	pr(border, "Generating the parameters, it's time consuming ...")
	nbit = 256
	while True:
		_p = getPrime(255)
		p = 2 * _p + 1
		if isPrime(p):
			g = 2
			if pow(g, _p, p) != 1: break
			else: g += 1
	x = getRandomRange(2, p // 2)
	y = pow(g, x, p)

	B, l = [int(b) for b in bin(p)[2:]], 30
	
	MSG = "4lL crypt0sy5t3ms suck5 fr0m faul7 atTaCk5 :P"
	m = bytes_to_long(MSG.encode('utf-8'))

	while True:
		pr("| Options: \n|\t[A]pply fault \n|\t[G]et the parameters \n|\t[S]ign the message \n|\t[V]erify the signature \n|\t[Q]uit")
		ans = sc().lower()
		if ans == 'a':
			_B = B
			pr(border, f"please send at most {l}-tuple array from indices of bits of ElGamal modulus, like: 5, 12, ...")
			ar = sc()
			try:
				ar = [int(_) for _ in ar.split(',')]
				if len(ar) <= l:
					for i in range(len(ar)): _B[ar[i]] = (_B[ar[i]] + 1) % 2
					P = int(''.join([str(b) for b in _B]), 2)
					Y = pow(g, x, P)
				else: raise Exception('Invalid length!')
			except: pr(border, "Something went wrong!!")
		elif ans == 'g':
			pr(border, f'p = {p}')
			pr(border, f'g = {g}')
			pr(border, f'y = {y}')
		elif ans == "v":
			pr(border, "please send signature to verify: ")
			_flag, signature = False, sc()
			try:
				signature = [int(_) for _ in signature.split(',')]
				if verify_esa((g, P, Y), signature, m): _flag = True
				else: pr(border, "Your signature is not valid!!")
			except:
				pr(border, "Something went wrong!!")
			if _flag: die(border, "Congrats! your got the flag: " + flag)
		elif ans == 's':
			pr(border, "Please send your message to sign: ")
			msg = sc().encode('utf-8')
			if msg != MSG.encode('utf-8'):
				_m = bytes_to_long(msg)
				try:
					sgn = sign_esa((g, P, Y), x, _m)
					pr(border, f'sign = {sgn}')
				except:
					pr(border, "Something went wrong!!")
			else:
				pr(border, "Kidding me!? Really?")
		elif ans == 'q': die("Quitting ...")
		else: die("Bye bye ...")

if __name__ == "__main__": main()