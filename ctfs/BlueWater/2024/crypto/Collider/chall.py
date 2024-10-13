from secret import flag
import random, os
os.urandom = random.randbytes
random.seed(int(input("> "), 16))
# Thanks y011d4!

from Crypto.Util.number import *
from sympy import GF, ZZ, Poly
from sympy.abc import x

# https://en.wikipedia.org/wiki/Factorization_of_polynomials_over_finite_fields#Rabin's_test_of_irreducibility
def is_irr(poly):
	from sympy.polys.galoistools import gf_pow_mod

	q = int(poly.get_modulus())
	deg = poly.degree()

	# x^exp mod g on GF(q)
	x_modpow = lambda exp, g: Poly(gf_pow_mod(ZZ.map([1, 0]), exp, ZZ.map(g.all_coeffs()), q, ZZ), x, modulus=q)
	x_gf = Poly(x, x, modulus=q)

	for p in range(deg, 0, -1):
		if deg % p == 0 and isPrime(p):
			if poly.gcd(x_modpow(q**(deg // p), poly) - x_gf) != 1:
				return False

	if (x_modpow(q**deg, poly) - x_gf) % poly != 0:
		return False
	return True

def input_irr(deg, F):
	while poly := Poly([1] + list(map(int, input("> ").split(", ")[:deg]))[::-1], x, domain=F):
		if is_irr(poly): return poly

def rand_irr(deg, F):
	while poly := Poly([1] + [getRandomRange(0, F.mod) for _ in range(deg)][::-1], x, domain=F):
		if is_irr(poly): return poly

def phase(msg):
	print(msg)

	F = GF(getStrongPrime(1024))
	deg = 4

	p1, q1 = [rand_irr(deg, F) for _ in range(2)]
	print(f"n = {p1 * q1}")
	p2, q2 = [input_irr(deg, F) for _ in range(2)]

	assert p1 * q1 == p2 * q2
	return ((p1, q1) == (p2, q2)) or ((p1, q1) == (q2, p2))

if __name__ == "__main__":
	assert phase("--- Phase 1 ---")
	assert not phase("--- Phase 2 ---")
	print(flag)
