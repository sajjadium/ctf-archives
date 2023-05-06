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

def main():
	border = "|"
	pr(border*72)
	pr(border, "Hi all, now it's time to solve a relatively simple challenge about  ", border)
	pr(border, "relatively elliptic curves! We will generate an elliptic curve with ", border)
	pr(border, "your desired parameters, are you ready!?                            ", border)
	pr(border*72)

	nbit = 256
	q = getPrime(nbit)
	F = GF(q)

	while True:
		pr(border, "Send the `y' element of two points in your desired elliptic curve:  ")
		ans = sc()
		try:
			y1, y2 = [int(_) % q for _ in ans.split(b',')]
		except:
			die(border, "Your parameters are not valid! Bye!!")
		A = (y1**2 - y2**2 - 1337**3 + 31337**3) * inverse(-30000, q) % q
		B = (y1**2 - 1337**3 - A * 1337) % q
		E = EllipticCurve(GF(q), [A, B])
		G = E.random_point()

		m = bytes_to_long(flag)
		assert m < q
		C = m * G
		pr(border, f'The parameters and encrypted flag are:')
		pr(border, f'q = {q}')
		pr(border, f'G = ({G.xy()[0]}, {G.xy()[1]})')
		pr(border, f'm * G = ({C.xy()[0]}, {C.xy()[1]})')

		pr(border, f'Now find the flag :P')

if __name__ == '__main__':
	main()