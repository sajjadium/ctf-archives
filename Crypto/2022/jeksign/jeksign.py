#!/usr/bin/env python3

from Crypto.Util.number import *
from secret import gensol, nbit_gensol
from flag import flag

m = bytes_to_long(flag.encode('utf-8'))
print(m)

a = 1337
b = 31337

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
	pr(border, "Welcome crypto guys! Here we are looking for the solution of special", border)
	pr(border, "Diophantine equation: 1337(z^4 - x^2) = 31337(y^2 - z^4) in natural ", border)
	pr(border, "numbers, in each stage solve the equation in mentioned interval :)  ", border)
	pr(border*72)

	STEP, level = 0, 19

	while True:
		p, q = nbit_gensol(1337, 31337, STEP + 30)
		x, y, z = gensol(a, b, p, q)
		pr(border, f"Send a solution like `x, y, z' such that the `z' is {STEP + 30}-bit: ")
		ans = sc()
		try:
			X, Y, Z = [int(_) for _ in ans.split(',')]
			NBIT = Z.bit_length()
		except:
			die(border, 'Your input is not valid, Bye!')
		if 1337*(Z**4 - X**2) == 31337*(Y**2 - Z**4) and NBIT == STEP + 30:
			if STEP == level - 1:
				die(border, f'Congrats, you got the flag: {flag}')
			else:
				pr('| good job, try to solve the next challenge :P')
				STEP += 1
		else:
			die(border, 'your answer is not correct, Bye!!')

if __name__ == '__main__':
	main()