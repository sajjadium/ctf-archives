#!/usr/bin/env python3

import random
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

def check_inputs(a, b, c):
	if not all(isinstance(x, int) for x in [a, b, c]):
		return False
	if a == 0 or b == 0 or c == 0:
		return False
	if a == b or b == c or a == c:
		return False
	return True

def check_solution(a, x, y, z):
	return (x*x + y*y - x*y - a*(z**3)) == 0

def main():
	border = "|"
	pr(border*72)
	pr(border, ".::   Hi all, she DID it, you should do it too! Are you ready? ::.  ", border)
	pr(border, "Welcome to the Ternary World! You need to pass each level until 20  ", border)
	pr(border, "to get the flag. Pay attention that your solutions should be nonzero", border)
	pr(border, "distinct integers. Let's start!                                     ", border)
	pr(border*72)

	level, step = 0, 19
	while level <= step:
		a = random.randint(2**(level * 12), 2**(level*12 + 12))
		equation = f'x^2 + y^2 - xy = {a}*z^3'
		pr(f"Level {level + 1}: {equation}")
		inputs = input().strip().split(",")
		try:
			x, y, z = map(int, inputs)
		except:
			die(border, "Invalid input, Bye!!")
		if check_inputs(x, y, z):
			if check_solution(a, x, y, z):
				pr(border, "Correct! Try the next level :)")
				level += 1
			else:
				pr(border, "You didn't provide the correct solution.")
				die(border, "Better luck next time!")			
		else:
			pr(border, "Your solutions should be non-zero distinct integers")
			die(border, "Quiting...")
		if level == step:
			pr(border, "Congratulations! You've successfully solved all the equations!")
			die(border, f"flag: {flag}")

if __name__ == '__main__':
	main()