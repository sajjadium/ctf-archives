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
	pr(border, " Greetings and welcome to the Renamiara cryptography challenge! The ", border)
	pr(border, " objective of this mission is to tackle an exceptionally difficult  ", border)
	pr(border, " and unique discrete logarithm problem in the real world. Are you   ", border)
	pr(border, " prepared and willing to take on this challenge? [Y]es or [N]o?     ", border)
	pr(border*72)


	ans = sc().decode().strip().lower()
	if ans == 'y':
		NBIT = 32
		STEP = 40

		pr(border, "In each step solve the given equation and send the solution for x, y", border)
		c = 1
		while c <= STEP:
			nbit = NBIT * c
			p = getPrime(nbit)
			pr(border, f'p = {p}')
			pr(border, 'First send the base g: ')
			g = sc().strip().decode()
			pr(border, 'Send the solutions for pow(g, x + y, p) = x * y, as x and y:')
			xy = sc().strip().decode().split(',')
			try:
				g, x, y = [int(_) for _ in [g] + xy]
			except:
				die(border, 'Given number is not correct! Bye!!')
			if (x >= p-1 or x <= 1) or (y >= p-1 or y <= 1) or x == y:
				die(border, "Kidding me!? Your solutions must be smaller than p-1 and x ≠ y :(")
			if g <= 2**24 or g >= p-1:
				die(border, "Kidding me!? Please send the correct base :P")
			if pow(g, x + y, p) ==  x * y % p:
				if c == STEP:
					die(border, f"Congratulation! the flag is: {flag}")
				else:
					pr(border, "Good job, try to solve the next level!")
					c += 1
			else:
				die(border, "Try harder and be smarter to find the solution!!")
	elif ans == 'n':
		pr(border, 'Bye!!')
	else:
		pr(border, 'Please send a valid answer! Bye!!')

if __name__ == '__main__':
	main()