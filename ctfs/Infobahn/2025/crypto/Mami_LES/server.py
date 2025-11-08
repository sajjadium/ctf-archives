from Crypto.Cipher import AES
from Crypto.Util.number import getPrime, getRandomRange
from Crypto.Util.Padding import pad
from hashlib import sha256
from os import getenv

class Mami_LES:
	def __init__(self, block_len, pad_len, p, secret):
		self.block_len = block_len
		self.pad_len = pad_len
		self.p = p
		self.iv = list(pow(secret + i, 1500, p) for i in range(block_len))
		self.iv_inv = [pow(x, -1, p) for x in self.iv]
	def encrypt(self, plaintext):
		assert len(plaintext) == self.block_len
		state = list(map(int, plaintext))
		for jump in range(1, self.block_len):
			for i in range(jump, self.block_len):
				state[i] += state[i - jump]
				if state[i] >= self.p:
					state[i] -= self.p
		return list(a * b % self.p for a, b in zip(state, self.iv))
	def decrypt(self, ciphertext):
		assert len(ciphertext) == self.block_len
		state = list(a * b_inv % self.p for a, b_inv in zip(ciphertext, self.iv_inv))
		for jump in reversed(range(1, self.block_len)):
			for i in reversed(range(jump, self.block_len)):
				state[i] -= state[i - jump]
				if state[i] < 0:
					state[i] += self.p
		return state
	def randomly_pad(self, text):
		assert self.pad_len + len(text) <= self.block_len
		padded_text = list(map(int, text))
		while self.pad_len + len(padded_text) < self.block_len:
			padded_text.insert(getRandomRange(0, len(padded_text) + 1), getRandomRange(1, self.p))
		return [getRandomRange(1, self.p) for _ in range(self.pad_len)] + padded_text

if __name__ == "__main__":
	flag = getenv("FLAG", "infobahn{fake_flag}")
	assert flag.startswith("infobahn{") and flag.endswith("}")

	nbit, block_len, pad_len = 512, 100, 14
	p = getPrime(nbit)
	secret = getRandomRange(1, p)
	ML = Mami_LES(block_len, pad_len, p, secret)

	print(AES.new(sha256(hex(secret).encode()).digest()[:16], AES.MODE_ECB).encrypt(pad(flag.encode(), 16)).hex())

	for _ in range(2000):
		mode = input("MODE(E/D)> ")
		text = list(int(x) % p for x in input("TEXT> ").split(" "))
		assert len(text) <= 50
		if mode == "E":
			print(ML.encrypt(ML.randomly_pad(text))[ML.pad_len:])
		elif mode == "D":
			print(ML.decrypt(ML.randomly_pad(text))[ML.pad_len:])
		else:
			break
