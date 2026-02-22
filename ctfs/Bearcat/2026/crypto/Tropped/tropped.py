import random
n = 64

class TropMatrix:

	def __init__(self, mat):
		self.mat = mat
		self.m = len(self.mat)
		self.n = len(self.mat[0])

	def __mul__(self, other):
		if self.n != other.m:
			print("Matrix dimensions do not match")
			exit()

		res = [[min(a+b for a, b in zip(rA, cB)) for cB in zip(*other.mat)] for rA in self.mat]
		return TropMatrix(res)

def generateM():
	M = TropMatrix([[random.randint(-255, 255) for _ in range(n)] for _ in range(n)])
	return M

def generatea():
	a = TropMatrix([[random.randint(-255, 255) for _ in range(n)]])
	return a

def generateb():
	b = TropMatrix([[random.randint(-255, 255)] for _ in range(n)])
	return b

def decryptByte(aMb, enc_byte):
	pt_byte = chr((aMb.mat[0][0] % 32) ^ ord(enc_byte))
	return pt_byte
