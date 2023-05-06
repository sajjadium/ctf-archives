#!/usr/bin/env python3

from Crypto.Util.number import *
from random import randint
import sys
from flag import FLAG

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
	pr(border, " hi talented cryptographers, the mission is to find the three RSA   ", border)
	pr(border, " modulus with the same public and private exponent! Try your chance!", border)
	pr(border*72)

	nbit = 160

	while True:
		pr("| Options: \n|\t[S]end the three nbit prime pairs \n|\t[Q]uit")
		ans = sc().lower()
		order = ['first', 'second', 'third']
		if ans == 's':
			P, N = [], []
			for i in range(3):
				pr("| Send the " + order[i] + " RSA primes such that nbit >= " + str(nbit) + ": p_" + str(i+1) + ", q_" + str(i+1) + " ")
				params = sc()
				try:
					p, q = params.split(',')
					p, q = int(p), int(q)
				except:
					die("| your primes are not valid!!")
				if isPrime(p) and isPrime(q) and len(bin(p)[2:]) >= nbit and len(bin(q)[2:]) >= nbit:
					P.append((p, q))
					n = p * q
					N.append(n)
				else:
					die("| your input is not desired prime, Bye!")
			if len(set(N)) == 3:
				pr("| Send the public and private exponent: e, d ")
				params = sc()
				try:
					e, d = params.split(',')
					e, d = int(e), int(d)
				except:
					die("| your parameters are not valid!! Bye!!!")
				phi_1 = (P[0][0] - 1)*(P[0][1] - 1)
				phi_2 = (P[1][0] - 1)*(P[1][1] - 1)
				phi_3 = (P[2][0] - 1)*(P[2][1] - 1)
				if 1 < e < min([phi_1, phi_2, phi_3]) and 1 < d < min([phi_1, phi_2, phi_3]):
					b = (e * d % phi_1 == 1) and (e * d % phi_2 == 1) and (e * d % phi_3 == 1)
					if b:
						die("| You got the flag:", FLAG)
					else:
						die("| invalid exponents, bye!!!")
				else:
					die("| the exponents are too small or too large!")
			else:
				die("| kidding me?!!, bye!")
		elif ans == 'q':
			die("Quitting ...")
		else:
			die("Bye ...")

if __name__ == '__main__':
	main()