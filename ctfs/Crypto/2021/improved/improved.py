#!/usr/bin/env python3

from Crypto.Util.number import *
from gmpy2 import gcd
from random import randint
import sys, hashlib
from flag import flag

def lcm(a, b):
	return (a * b) // gcd(a,b)

def gen_params(nbit):
	p, q = [getPrime(nbit) for _ in range(2)]
	n, f, g = p * q, lcm(p-1, q-1), p + q
	e = pow(g, f, n**2)
	u = divmod(e-1, n)[0]
	v = inverse(u, n)
	params = int(n), int(f), int(v)
	return params

def improved(m, params):
	n, f, v = params
	if 1 < m < n**2 - 1:
		e = pow(m, f, n**2)
		u = divmod(e-1, n)[0]
		L = divmod(u*v, n)[1]
	H = hashlib.sha1(str(L).encode('utf-8')).hexdigest()
	return H

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
	pr(border, " hi talented cryptographers! Your mission is to find hash collision ", border)
	pr(border, " in the given hash function based on famous cryptographic algorithm ", border)
	pr(border, " see the source code and get the flag! Its improved version :)      ", border)
	pr(border*72)

	nbit = 512
	params = gen_params(nbit)
	n = params[0]

	while True:
		pr("| Options: \n|\t[R]eport collision! \n|\t[T]ry hash \n|\t[G]et parameters \n|\t[Q]uit")
		ans = sc().lower()
		if ans == 'r':
			pr("| please send the messages split by comma: ")
			m = sc()
			try:
				m_1, m_2 = m.split(',')
				m_1, m_2 = int(m_1), int(m_2)
			except:
				die("| Sorry! your input is invalid, Bye!!")
				# fix the bug :P
			if m_1 % n != 0 and m_2 % n != 0 and m_1 != m_2 and 1 < m_1 < n**2-1 and 1 < m_2 < n**2-1 and improved(m_1, params) == improved(m_2, params):
				die(f"| Congrats! You find the collision!! the flag is: {flag}")
			else:
				die("| Sorry! your input is not correct!!")
		elif ans == 't':
			pr("| Please send your message to get the hash: ")
			m = sc()
			try:
				m = int(m)
				pr(f"improved(m) = {improved(m, params)}")
			except:
				die("| Sorry! your input is invalid, Bye!!") 
		elif ans == 'g':
			pr('| Parameters =', params)
		elif ans == 'q':
			die("Quitting ...")
		else:
			die("Bye ...")

if __name__ == '__main__':
	main()