#!/usr/bin/env python3
# In the name of Allah

from mini_ecdsa import *
from Crypto.Util.number import *
from flag import flag

def tonelli_shanks(n, p):
	if pow(n, int((p-1)//2), p) == 1:
			s = 1
			q = int((p-1)//2)
			while True:
				if q % 2 == 0:
					q = q // 2
					s += 1
				else:
					break
			if s == 1:
				r1 = pow(n, int((p+1)//4), p)
				r2 = p - r1
				return r1, r2
			else:
				z = 2
				while True:
					if pow(z, int((p-1)//2), p) == p - 1:
						c = pow(z, q, p)
						break
					else:
						z += 1
				r = pow(n, int((q+1)//2), p)
				t = pow(n, q, p)
				m = s
				while True:
					if t == 1:
						r1 = r
						r2 = p - r1
						return r1, r2
					else:
						i = 1
						while True:
							if pow(t, 2**i, p) == 1:
								break
							else:
								i += 1
						b = pow(c, 2**(m-i-1), p)
						r = r * b % p
						t = t * b ** 2 % p
						c = b ** 2 % p
						m = i
	else:
		return False

def random_point(p, a, b):
	while True:
		gx = getRandomRange(1, p-1)
		n = (gx**3 + a*gx + b) % p
		gy = tonelli_shanks(n, p)
		if gy == False:
			continue
		else:
			return (gx, gy[0])

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
	border = "+"
	pr(border*72)
	pr(border, "  Dual ECC means two elliptic curve with same coefficients over the ", border)
	pr(border, "  different fields or ring! You should calculate the discrete log   ", border)
	pr(border, "  in dual ECCs. So be smart in choosing the first parameters! Enjoy!", border)
	pr(border*72)

	bool_coef, bool_prime, nbit = False, False, 128
	while True:
		pr(f"| Options: \n|\t[C]hoose the {nbit}-bit prime p \n|\t[A]ssign the coefficients \n|\t[S]olve DLP \n|\t[Q]uit")
		ans = sc().lower()
		if ans == 'a':
			pr('| send the coefficients a and b separated by comma: ')
			COEFS = sc()
			try:
				a, b = [int(_) for _ in COEFS.split(',')]
			except:
				die('| your coefficients are not valid, Bye!!')
			if a*b == 0:
				die('| Kidding me?!! a*b should not be zero!!')
			else:
				bool_coef = True
		elif ans == 'c':
			pr('| send your prime: ')
			p = sc()
			try:
				p = int(p)
			except:
				die('| your input is not valid :(')
			if isPrime(p) and p.bit_length() == nbit and isPrime(2*p + 1):
				q = 2*p + 1
				bool_prime = True
			else:
				die(f'| your integer p is not {nbit}-bit prime or 2p + 1 is not prime, bye!!')
		elif ans == 's':
			if bool_coef == False:
				pr('| please assign the coefficients.')
			if bool_prime == False:
				pr('| please choose your prime first.')
			if bool_prime and bool_coef:
				Ep = CurveOverFp(0, a, b, p)
				Eq = CurveOverFp(0, a, b, q)

				xp, yp = random_point(p, a, b)
				P = Point(xp, yp)

				xq, yq = random_point(q, a, b)
				Q = Point(xq, yq)

				k = getRandomRange(1, p >> 1)
				kP = Ep.mult(P, k)

				l = getRandomRange(1, q >> 1)
				lQ = Eq.mult(Q, l)
				pr('| We know that: ')
				pr(f'| P = {P}')
				pr(f'| k*P = {kP}')
				pr(f'| Q = {Q}')
				pr(f'| l*Q = {lQ}')
				pr('| send the k and l separated by comma: ')
				PRIVS = sc()
				try:
					priv, qriv = [int(s) for s in PRIVS.split(',')]
				except:
					die('| your input is not valid, Bye!!')
				if priv == k and qriv == l:
					die(f'| Congrats, you got the flag: {flag}')
				else:
					die('| sorry, your keys are not correct! Bye!!!')
		elif ans == 'q':
			die("Quitting ...")
		else:
			die("Bye ...")

if __name__ == '__main__':
	main()