import numpy as np

n = 640
q = 1 << 15
sigma = 2.75

public = lambda: np.random.randint(q, size=(n, n))
secret = lambda: np.random.randint(q, size=n)
error = lambda: np.rint(np.random.normal(0, sigma, n)).astype(int)

def add(x, y):
	return np.mod(x+y, q)

def mul(A, x):
	return np.mod(np.matmul(A, x), q)

def sample(A):
	s = secret()
	b = add(mul(A, s), error())
	return s, b