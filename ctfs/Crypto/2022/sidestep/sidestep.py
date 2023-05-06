#!/usr/bin/env python3

from Crypto.Util.number import *
import random, sys
from flag import flag

def pow_d(g, e, n):
	t, r = 0, 1
	for _ in bin(e)[2:]:
		if r == 4: t += 1
		r = pow(r, 2, n)
		if _ == '1': r = r * g % n
	return t, r

def ts(m, p):
	m = m % p
	return pow(m, (p - 1) // 2, p) == 1

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
	pr(border, "Hi all cryptographers! Welcome to the Sidestep task, we do powing!!!", border)
	pr(border, "You should solve a DLP challenge in some special way to get the flag", border)

	p = 2 ** 1024 - 2 ** 234 - 2 ** 267 - 2 ** 291 - 2 ** 403 - 1
	s = random.randint(2, (p - 1) // 2)

	while True:
		pr("| Options: \n|\t[T]ry the magic machine \n|\t[Q]uit")
		ans = sc().lower()

		if ans == 't':
			pr(border, "please send your desired integer: ")
			g = sc()
			try:
				g = int(g)
			except:
				die(border, "The given input is not integer!")
			if ts(g, p):
				t, r = pow_d(g, s, p)
				if r == 4:
					die(border, f'Great! you got the flag: {flag}')
				else:
					pr(border, f"t, r = {t, r}")
			else:
				pr(border, "The given base is NOT valid!!!")
		elif ans == 'q':
			die(border, "Quitting ...")
		else:
			die(border, "Bye bye ...")

if __name__ == "__main__":
	main()