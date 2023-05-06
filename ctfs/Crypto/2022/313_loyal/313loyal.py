#!/usr/bin/env python3

from Crypto.Util.number import *
from random import *
import sys
from flag import flag

def keygen(nbit):
	p, q = [getPrime(nbit) for _ in '__']
	n, phi = p * q, (p - 1) * (q - 1) // 2
	while True:
		g = getRandomRange(2, n ** 2)
		if GCD(g, n) == 1:
			w = (pow(g, phi, n ** 2) - 1) // n
			if GCD(w, n) == 1:
				u = inverse(w, n)
				break
	pkey, skey = (n, g), (phi, u)
	return pkey, skey

def encrypt(pkey, m):
	n, g = pkey
	while True:
		r = getRandomRange(2, n)
		if GCD(r, n) == 1:
			break
	return (pow(g, m, n ** 2) * pow(r, n, n ** 2)) % (n ** 2)

def add(pkey, a, b):
	n, g = pkey
	return pow(a * b, 1, n ** 2)

def multiply(pkey, a, k):
	n, g = pkey
	return pow(a, k, n ** 2)

def mul_poly(n, P, Q):
	R = [0] * (len(P) + len(Q))
	for i in range(len(P)):
		for j in range(len(y)):
			R[i+j] += (R[i + j] + P[i] * Q[j]) % n
	return R

def encrypt_poly(pkey, poly):
	return [encrypt(pkey, term) for term in poly]

def client_genpoly(pkey, points):
	n, g = pkey
	result = [1]
	for point in points:
		result = mul_poly(n, result, [-point, 1])
	return encrypt_poly(pkey, result)

def evaluate_poly(pkey, poly, point):
	n, g = pkey
	_point = point
	result = poly[0]
	for term in poly[1:]:
		result = add((n, g), result, multiply((n, g), term, _point))
		_point = (_point * point) % n
	return result

def backend(pkey, poly, points):
	n, g = pkey
	R = []
	for point in points:
		result = evaluate_poly((n, g), poly, point)
		result = multiply((n, g), result, getRandomRange(2, n))
		result = add((n, g), result, encrypt((n, g), point))
		R.append(result)
	return R

def main():
	border = "|"
	pr(border*72)
	pr(border, " Hi cryptographers, our mission is analyzing a modern crypto-system ", border)
	pr(border, " with given parameters, be motivated and try to grab the flag!      ", border)
	pr(border*72)
	nbit = 256
	while True:
		POINTS = []
		for i in range(len(flag)):
			POINTS.append(getRandomRange(2, 2 ** 64) * 2 ** 10)
		POINTS.sort()
		for i in range(len(flag)):
			POINTS[i] += flag[i]
		pr("| Options: \n|\t[S]end parameters and try the oracle \n|\t[Q]uit")
		ans = sc().lower()
		if ans == 's':
			pr(border, "Send the parameters of crypto-system like: n, g, poly ")
			params = sc()
			try:
				n, g, poly = params.split(',')
				n, g, poly = int(n), int(g), poly.strip()
				poly = list(map(int, poly.replace('[', '').replace(']', '').split(' ')))
				if (n < 2 ** nbit):
					die(border, "n is too small :(")
				pkey = (n, g)
				result = backend(pkey, poly, POINTS)
				shuffle(result)
			except:
				die(border, "your parameters are not valid!!")
			for i in range(len(result)):
				pr(border, f'result[{i}] = {result[i]}')
		elif ans == 'q':
			die(border, "Quitting ...")
		else:
			die(border, "Bye ...")

def die(*args):
	pr(*args)
	quit()

def pr(*args):
	s = " ".join(map(str, args))
	sys.stdout.write(s + "\n")
	sys.stdout.flush()

def sc():
	return sys.stdin.readline().strip()

if __name__ == '__main__':
	main()