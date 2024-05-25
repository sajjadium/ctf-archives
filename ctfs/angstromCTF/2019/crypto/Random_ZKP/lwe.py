import numpy as np
import os

from Crypto.Util.number import getRandomInteger

n = 640
b = 15
q = 1 << b
sigma = 2.75

public = lambda: np.array([[getRandomInteger(b) for _ in range(n)] for _ in range(n)])
secret = lambda: np.array([getRandomInteger(b) for _ in range(n)])
def error():
	np.random.seed(getRandomInteger(32))
	return np.rint(np.random.normal(0, sigma, n)).astype(int)

def add(x, y):
	return np.mod(x+y, q)

def mul(A, x):
	return np.mod(np.matmul(A, x), q)

def sample(A):
	s = secret()
	b = add(mul(A, s), error())
	return s, b