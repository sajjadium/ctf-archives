import random
from data import e, N, v, A, l, a, b, m1, m2, h


# this looks familiar
def rsa_encrypt(plaintext):
	return plaintext^e


# but what about this????
def rsa_decrypt(ciphertext):
	M = matrix(A)
	s = vector([m1^i * sum([binomial(i, j) * a^j * ciphertext^(h * j) * b^(i - j) for j in range(i + 1)]) for i in range(M.ncols())])
	u = M * s + a^(M.nrows()) * ciphertext^(h * M.nrows()) * vector(v)
	return reduce(lambda x, y: x^(M.nrows()) * u[y], [1] + l) * m2


if __name__ == "__main__":
	# let's see if this works
	for _ in range(10):
		p = Integers(N).random_element()
		assert rsa_decrypt(rsa_encrypt(p)) == p

	print("yey my RSA works!!")
