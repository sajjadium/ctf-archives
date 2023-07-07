#!/usr/bin/env python3

import sys
import random
import binascii
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

def vinefruit(msg, mod, flag = 0):
	P = [16777619, 1099511628211, 309485009821345068724781371]
	O = [2166136261, 14695981039346656037, 144066263297769815596495629667062367629]
	assert mod in [0, 1, 2]
	p, o, m = P[mod], O[mod], 2 ** (2 << (4 + mod))
	vine = o
	for b in msg:
		if flag == 1:
			vine = (vine + b) % (2 ** 128)
		else:
			vine = vine ^ b
		vine = (vine * p) % m
	return vine

def main():
	border = "|"
	pr(border*72)
	pr(border, " Hi all, I have designed a gorgeous cryptography hash function in   ", border)
	pr(border, " order to secure the world! Your mission is to find collision for   ", border)
	pr(border, " this function with specific conditions.                            ", border)
	pr(border*72)
	
	step = 19

	while True:
		pr("| Options: \n|\t[S]ubmit collision \n|\t[Q]uit")
		ans = sc().decode().lower().strip()
		if ans == 's':
			S = []
			for level in range(step):
				mod = random.randint(0, 2)
				pr(border, f'Submit two different string such that vinefruit(m1, {mod}, 1) = vinefruit(m2, {mod}, 1)')
				pr(border, f'You are at level: {level + 1}')
				if level == step - 1 and len(S) == step - 1:
					die(border, f'Congrats, you got the flag: {flag}')
				try:
					pr(border, f'Please send first byte string: ')
					s1 = sc()[:-1]
					pr(border, f'Please send second byte string: ')
					s2 = sc()[:-1]
					s1, s2 = binascii.unhexlify(s1), binascii.unhexlify(s2)
				except:
					pr(border, 'You should send valid hex strings.')
					break
				if len(s1) == len(s2) == 35 - level and s1 != s2:
					if vinefruit(s1, mod, 1) == vinefruit(s2, mod, 1):
						if vinefruit(s1, mod, 1) not in S:
							S.append(vinefruit(s1, mod, 1))
							pr(border, 'gj, try the next level :)')
						else:
							break
					else:
						break
				else:
					die(border, 'Kidding me?! Try again and be smart!! Bye!!!')
		elif ans == 'q':
			die(border, 'Quitting...')
		else:
			die(border, 'You should select valid choice!')

if __name__ == '__main__':
	main()