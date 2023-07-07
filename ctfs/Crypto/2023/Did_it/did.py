#!/usr/bin/env python3

from random import randint
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

def did(n, l, K, A):
	A, K = set(A), set(K)
	R = [pow(_, 2, n) + randint(0, 1) for _ in A - K]
	return R

def main():
	border = "+"
	pr(border*72)
	pr(border, ".::   Hi all, she DID it, you should do it too! Are you ready? ::.  ", border)
	pr(border*72)

	_flag = False
	n, l = 127, 20
	N = set(list(range(0, n)))
	K = [randint(0, n-1) for _ in range(l)]
	cnt, STEP = 0, 2 * n // l - 1
	
	while True:
		ans = sc().decode().strip()
		try:
			_A = [int(_) for _  in ans.split(',')]
			if len(_A) <= l and set(_A).issubset(N):
				DID = did(n, l, K, _A)
				pr(border, f'DID = {DID}')
				if set(_A) == set(K):
					_flag = True
			else:
				die(border, 'Exception! Bye!!')
		except:
			die(border, 'Your input is not valid! Bye!!')
		if _flag:
			die(border, f'Congrats! the flag: {flag}')
		if cnt > STEP:
			die(border, f'Too many tries, bye!')
		cnt += 1

if __name__ == '__main__':
	main()