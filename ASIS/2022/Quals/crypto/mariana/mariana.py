#!/usr/bin/env python3

from Crypto.Util.number import *
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
	return sys.stdin.buffer.readline()

def main():
	border = "|"
	pr(border*72)
	pr(border, "Welcome to MARIANA cryptography battle, the mission is solving super", border)
	pr(border, "hard special DLP problem in real world, are you ready to fight?     ", border)
	pr(border*72)

	NBIT = 32
	STEP = 40

	pr(border, "In each step solve the given equation and send the solution for x.  ", border)
	c = 1
	while c <= STEP:
		nbit = NBIT * c
		p = getPrime(nbit)
		g = getRandomRange(3, p)
		pr(border, f'p = {p}')
		pr(border, f'g = {g}')
		pr(border, 'Send the solution x = ')
		ans = sc()
		try:
			x = int(ans)
		except:
			die(border, 'Given number is not integer!')
		if x >= p:
			die(border, "Kidding me!? Your solution must be smaller than p :P")
		if (pow(g, x, p) - x) % p == 0:
			if c == STEP:
				die(border, f"Congratz! the flag is: {flag}")
			else:
				pr(border, "Good job, try to solve the next level!")
				c += 1
		else:
			die(border, "Try harder and smarter to find the solution!")

if __name__ == '__main__':
	main()