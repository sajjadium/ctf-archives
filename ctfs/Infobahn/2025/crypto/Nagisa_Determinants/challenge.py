from Crypto.Cipher import AES
from Crypto.Util.number import getPrime
from Crypto.Util.Padding import pad
from hashlib import sha256
from os import getenv
from random import randrange, shuffle
from sage.all import GF, ZZ, matrix

class Nagisa_Determinants:
	def __init__(self, p, key_len, output_len):
		self.p = p
		self.key_len = key_len
		self.output_len = output_len
	def determinants(self, key):
		assert len(key) == self.key_len
		secret = 0
		output = []
		pos = [(i, j) for i in range(self.key_len - 1) for j in range(i + 1, self.key_len - 1)]
		for _ in range(self.output_len):
			while True:
				shuffle(pos)
				S = matrix(ZZ        , self.key_len - 1, self.key_len - 1)
				O = matrix(GF(self.p), self.key_len - 2, self.key_len - 2)
				for (i, j), x in zip(pos, key):
					S[i, j] += 1
					S[j, i] += 1
					for ii, jj, delta in [(i, i, 1), (i, j, -1), (j, i, -1), (j, j, 1)]:
						if max(ii, jj) < self.key_len - 2:
							O[ii, jj] += delta * x
				if O.determinant() != 0 and O.determinant() not in output:
					break
			secret = secret << 1 | int((S**3).trace() == 12)
			output.append(O.determinant())
		return secret, output

if __name__ == "__main__":
	flag = getenv("FLAG", "infobahn{fake_flag}")
	assert flag.startswith("infobahn{") and flag.endswith("}")

	key_len, output_len = 8, 300
	p = getPrime(1024)
	ND = Nagisa_Determinants(p, key_len, output_len)
	key = [randrange(p) for _ in range(key_len)]

	secret, output = ND.determinants(key)
	print(output)
	print(AES.new(sha256(hex(secret).encode()).digest()[:16], AES.MODE_ECB).encrypt(pad(flag.encode(), 16)).hex())
