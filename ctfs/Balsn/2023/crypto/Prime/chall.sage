import gmpy2
import random
from secret import FLAG

def main():
	n = int(input("prime: "))

	if n <= 0:
		print("No mystiz trick")
	elif n.bit_length() < 256 or n.bit_length() > 512:
		print("Not in range")
	elif not is_prime(n):
		print("Not prime")
	else:
		x = int(input("factor: "))

		if x > 1 and x < n and n % x == 0:
			print("You got me")
			print(FLAG)
		else:
			print("gg")

def is_prime(n):
	# check if n = a^b for some a, b > 1
	for i in range(2, n.bit_length()):
		root, is_exact = gmpy2.iroot(n, i)
		if is_exact:
			return False

	rs = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
	return all(test(n, r) for r in rs)

def test(n, r):
	"""
	check whether `(x + a) ^ n = x ^ n + a (mod x ^ r - 1)` in Z/nZ for some `a`.
	"""
	R.<x> = Zmod(n)[]
	S = R.quotient_ring(x ^ r - 1)

	a = 1 + random.getrandbits(8)
	if S(x + a) ^ n != S(x ^ (n % r)) + a:
		return False
	return True

if __name__ == "__main__":
	main()