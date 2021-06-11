#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import random, sys, os, signal, string, re
import inspect
from flag import flag
import primefac

def tom(n):
	c = (n % 2) ^ 1
	while True:
		FU = list(primefac.primefac(n + c))
		FD = list(primefac.primefac(n - c))
		if len(FU) == 2:
			return c, FU
		elif len(FD) == 2:
			return c, FD
		else:
			c += 2

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
	step = 40
	c, border = 4, "+"
	pr(border*72)
	pr(border, " hi power programmers and coders! Your mission is to find a special ", border)
	pr(border, " number with desired property that we named it Tom. Now review the  ", border)
	pr(border, " source code and get the flag!                                      ", border)
	pr(border*72)

	while c <= step:
		r = random.randint(1, 20 + (c - 5))
		pr("| Send an integer `n' greater than", 11**c, "and less than", 11**(c+1), "such tom(n) =", r)
		ans = sc()
		try:
			ans = int(ans)
			if ans > 11**c and ans < 11**(c+1):
				if tom(ans)[0] == r:
					c += 1
					if c == step:
						die("| Congrats, you got the flag:", flag)
					else:
						pr("| good job, try the next level :)")
				else:
					print(tom(ans), r)
					die("| Your answer is not correct!", tom(ans)[0] == r)
			else:
				die("Quiting ...")
		except:
			die("Bye :P")

if __name__ == '__main__':
	main()