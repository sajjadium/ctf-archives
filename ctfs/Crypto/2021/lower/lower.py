#!/usr/bin/env python3

from Crypto.Util.number import *
import sys
from flag import flag

flag = flag.lstrip('CCTF{').rstrip('}')

def query(n, X, E, p):
	assert n == len(X) > len(E)
	C = [getRandomRange(0, p) for _ in range(n)]
	e = E[getRandomRange(0, len(E))]
	S = e
	for _ in range(n):
		S += X[_] * C[_]
		S %= p
	return C, S

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
	pr(border, " hi all, welcome to the learning by mistakes class of cryptography! ", border)
	pr(border, " try hard to find the flag by querying this oracle times and times!!", border)
	pr(border*72)

	p = 127
	E = [getRandomRange(0, p) for _ in range(5)]
	n = len(flag)
	X = [ord(c) for c in flag]

	while True:
		pr("| Options: \n|\t[Q]uery to oracle \n|\t[E]xit")
		ans = sc().lower()
		if ans == 'q':
			for i in range(12):
				pr(f'| Q_{i+1}: {query(n, X, E, p)}')
		elif ans == 'e':
			die("Exiting ...")
		else:
			die("Bye ...")

if __name__ == '__main__':
	main()