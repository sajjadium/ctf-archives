#!/usr/bin/env sage

import sys
from itertools import product
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

def slowsum(p, n):
	g = 0
	perms = list(product([0, 1], repeat = n))
	for _prm in perms:
		g += p(_prm)
	return g

def h4sh(p, q):
	coeffs = p.coefficients()
	return pow(sum(coeffs), (q - 1) // 2 - sum(coeffs), q) 

def main():
	border = "|"
	pr(border*72)
	pr(border, "Hi all, I have created a basic and rudimentary version of a sumcheck", border)
	pr(border, "protocol. Your task is to generate a false statement and persuade   ", border)
	pr(border, "verifier of its validity.                                           ", border)
	pr(border*72)
	
	q = 113
	F = GF(q)

	while True:
		pr("| Options: \n|\t[C]laim the statement \n|\t[D]etermine parameters and polynomial \n|\t[Q]uit")
		ans = sc().decode().lower().strip()
		if ans == 'd':
			pr(border, f'Please first send the number of variable and the degree of your desired polynomial:')
			_ans = sc()
			try:
				_n, _d = [int(_) for _ in _ans.split(b',')]
				if (_n * _d) // q < 0.1 and _n >= 5 and _d >= 3:
					R = PolynomialRing(F, _n, 'x')
					x = R.gens()
				else:
					raise Exception()
			except:
				die(border, 'The parameters are not consistent! Try again!!')
			pr(border, f'Now, please send the {_n}-variable polynomial as p: ')
			_p = sc().strip().decode()
			try:
				_p = R(_p)
				p = _p
				_deg = _p.degree(std_grading=True)
				if _deg != _d:
					raise Exception()
			except:
				die(border, 'The polynomial is not valid or does not hold true in the given situations!')
			g = slowsum(_p, _n)
		elif ans == 'c':
			pr(border, 'Please send the g: ')
			_g = sc()
			try:
				_g = int(_g)
				if _g == g:
					die(border, 'Kidding me?! Bye :P')
			except:
				die(border, 'Some exception occurred! Bye!!')
			_P, _H = [], []
			for i in range(_n):
				pr(border, f'Please send the (p_{i}, h4sh(p_{i}, q)): ')
				pr(border, f'Note that the variable of p_{i} should be x. ')
				_ph = sc().strip()
				try:
					_p, _h = [_.decode() for _  in _ph.split(b',')]
					_R = PolynomialRing(F, 'x')
					_p, _h = _R(_p), F(_h)
					if _p.degree() > _d:
						raise Exception()
					_P.append(_p)
					_H.append(_h)
				except:
					die(border, 'Some exception occurred! Bye!!')
			j = 0
			for i in range(_n):
				if i == 0:
					if _P[i](0) + _P[i](1) != _g or h4sh(_P[i], q) != _H[i]:
						break
				else:
					if _P[i](0) + _P[i](1) != _P[i-1](_H[i-1]) or h4sh(_P[i], q) != _H[i]:
						break
				j += 1
			if j < _n or p(_H) != _P[_n-1](_H[_n-1]):
				die(border, 'Oops, verifier believes that the polynomial is not valid! Bye!!')
			die(border, f'Congrats, here the flag: {flag}')
		elif ans == 'q':
			die(border, 'Quitting...')
		else:
			die(border, 'You should select valid choice!')

if __name__ == '__main__':
	main()