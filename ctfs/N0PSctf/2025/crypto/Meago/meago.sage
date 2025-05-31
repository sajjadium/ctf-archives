#!/usr/bin/env sage

import sys
from Crypto.Util.number import *
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

nbit = 100
prec = 4 * nbit
R = RealField(prec)

def meago(x, y):
	y = (x * y**2) ** R(1/3)
	x = (x * y**2) ** R(1/3)
	return x, y

def main():
	border = "┃"
	pr(        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
	pr(border, ".::             Welcome to Meago oracle challenge!            ::. ", border)
	pr(border, " You should analyze this oracle and manage it to obtain the flag! ", border)
	pr(        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
	m = bytes_to_long(flag)
	x0 = R(10 ** (-len(str(m))) * m)
	while True:
		y0 = abs(R.random_element())
		if y0 > x0: break
	assert len(str(x0)) == len(str(y0))
	c = 0
	pr(border, f'We know y0 = {y0}')
	while True:
		pr("| Options: \n|\t[M]eago \n|\t[Q]uit")
		ans = sc().decode().strip().lower()
		if ans == 'm':
			x, y = meago(x0, y0)
			x0, y0 = x, y
			c += 1
			if c <= 5:
				pr(border, f'Sorry, no info available here!')
			else: pr(border, f'y = {y}')
		elif ans == 'q': die(border, "Quitting...")
		else: die(border, "Bye...")

if __name__ == '__main__':
	main()