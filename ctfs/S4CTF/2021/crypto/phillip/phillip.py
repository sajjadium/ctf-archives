#!/usr/bin/env python3

from Crypto.Util.number import *
from gmpy2 import next_prime, gcd, lcm
from random import randint
import sys, os, signal
import inspect
from flag import flag

def make_params(nbit):
	p, q = [getPrime(nbit) for _ in range(2)]
	n, f, g = p * q, lcm(p-1, q-1), p + q
	e = pow(g, f, n**2)
	u = divmod(e-1, n)[0]
	v = inverse(u, n)
	params = int(n), int(f), int(v)
	return params

def phillip_hash(m, params):
	n, f, v = params
	if 1 < m < n**2 - 1:
		e = pow(m, f, n**2)
		u = divmod(e-1, n)[0]
		H = divmod(u*v, n)[1]
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
	pr(border, " hi young cryptographers,! Your mission is to find a hash collision ", border)
	pr(border, " in the given hash function based on famous cryptographic algorithm ", border)
	pr(border, " see the source code and get the flag!                              ", border)
	pr(border*72)

	nbit = 256
	params = make_params(nbit)
	n = params[0]

	while True:
		pr("| Options: \n|\t[H]ash function \n|\t[R]eport collision! \n|\t[T]ry hash \n|\t[G]et params \n|\t[P]arams function \n|\t[Q]uit")
		ans = sc().lower()
		if ans == 'h':
			pr(inspect.getsource(phillip_hash))
		elif ans == 'p':
			pr(inspect.getsource(make_params))
		elif ans == 'r':
			pr("| please send first msg: ")
			m_1 = sc()
			pr("| please send second msg:")
			m_2 = sc()
			try:
				m_1 = int(m_1)
				m_2 = int(m_2)
			except:
				die("| sorry! your input is invalid, Bye!!")
			if m_1 != m_2 and 1 < m_1 < n**2-1 and 1 < m_2 < n**2-1 and phillip_hash(m_1, params) == phillip_hash(m_2, params):
				die("| Congrats! You find the collision!! the flag is:", flag)
			else:
				die("| sorry! your input is invalid or wrong!!")
		elif ans == 't':
			pr("| please send your message to get the hash: ")
			m = sc()
			try:
				m = int(m)
				pr("phillip_hash(m) =", phillip_hash(m, params))
			except:
				die("| sorry! your input is invalid, Bye!!") 
		elif ans == 'g':
			pr('| params =', params)
		elif ans == 'q':
			die("Quiting ...")
		else:
			die("Bye ...")

if __name__ == '__main__':
	main()