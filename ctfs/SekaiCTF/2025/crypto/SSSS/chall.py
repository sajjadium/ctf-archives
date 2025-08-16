import random, os

p = 2 ** 256 - 189
FLAG = os.getenv("FLAG", "SEKAI{}")

def challenge(secret):
	t = int(input())
	assert 20 <= t <= 50, "Number of parties not in range"

	f = gen(t, secret)

	for i in range(t):
		x = int(input())
		assert 0 < x < p, "Bad input"
		print(poly_eval(f, x))

	if int(input()) == secret:
		print(FLAG)
		exit(0)
	else:
		print(":<")

def gen(degree, secret):
	poly = [random.randrange(0, p) for _ in range(degree + 1)]
	index = random.randint(0, degree)

	poly[index] = secret
	return poly

def poly_eval(f, x):
	return sum(c * pow(x, i, p) for i, c in enumerate(f)) % p

if __name__ == "__main__":
	secret = random.randrange(0, p)
	for _ in range(2):
		challenge(secret)