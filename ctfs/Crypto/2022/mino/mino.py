#!/usr/bin/env python3

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
	return sys.stdin.readline().strip()

def main():
	border = "|"
	pr(border*72)
	pr(border, "Hi crypto programmers! I'm looking for some very special permutation", border)
	pr(border, "p name MINO such that sum(p(i) * (-2)^i) = 0 from 0 to n - 1, for   ", border)
	pr(border, "example for n = 6, the permutation p = (4, 2, 6, 5, 3, 1) is MINO:  ", border)
	pr(border, "4*(-2)^0 + 2*(-2)^1 + 6*(-2)^2 + 5*(-2)^3 + 3*(-2)^4 + 1*(-2)^5 = 0 ", border)
	pr(border, "In each step find such permutation and send to server, if there is  ", border)
	pr(border, "NOT such permutation for given n, just send `TINP', good luck :)    ", border)
	pr(border*72)
	step, final = 3, 40
	while True:
		pr(border, f"Send a MINO permutation of length = {step} separated by comma: ")
		p = sc().split(',')
		if step % 3 == 1:
			if p == ['TINP']:
				if step == final: die(border, f"Congrats, you got the flag: {flag}")
				else:
					pr(border, "Great, try the next level :)")
					step += 1
			else:
				die(border, "the answer is not correct, bye!!!")
		elif len(p) == step:
			try:
				p = [int(_) for _ in p]
			except:
				pr(border, "the permutation is not valid")
			if set(p) == set([_ for _ in range(1, step + 1)]):
				S = 0
				for _ in range(step):
					S += p[_] * (-2) ** _
				if S == 0:
					if step == final: 
						die(border, f"Congrats, you got the flag: {flag}")
					else:
						pr(border, "Great, try the next level :)")
						step += 1
				else:
					die(border, "the answer is not correct, bye!!!")
			else:
				pr(border, "the permutation is not valid!!!")
		else:
			die(border, f"the length of permutation is not equal to {step}")

if __name__ == "__main__":
	main()