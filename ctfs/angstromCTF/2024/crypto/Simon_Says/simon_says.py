class Simon:

	n = 64
	m = 4
	z = 0b01100111000011010100100010111110110011100001101010010001011111

	def __init__(self, k, T):
		self.T = T
		self.k = self.schedule(k)

	def S(self, x, j):
		j = j % self.n
		return ((x << j) | (x >> (self.n - j))) & 0xffffffffffffffff

	def schedule(self, k):
		k = k[:]
		for i in range(self.m, self.T):
			tmp = self.S(k[i - 1], -3)
			if self.m == 4:
				tmp ^= k[i - 3]
			tmp ^= self.S(tmp, -1)
			zi = (self.z >> ((i - self.m) % 62)) & 1
			k.append(k[i - self.m] ^ tmp ^ zi ^ 0xfffffffffffffffc)
		return k

	def encrypt(self, x, y):
		for i in range(self.T):
			tmp = x
			x = y ^ (self.S(x, 1) & self.S(x, 8)) ^ self.S(x, 2) ^ self.k[i]
			y = tmp
		return x, y

def encrypt(simon, pt):
	ct = bytes()
	for i in range(0, len(pt), 16):
		x = int.from_bytes(pt[i:i+8], 'big')
		y = int.from_bytes(pt[i+8:i+16], 'big')
		x, y = simon.encrypt(x, y)
		ct += x.to_bytes(8, 'big')
		ct += y.to_bytes(8, 'big')
	return ct

if __name__ == '__main__':
	from random import SystemRandom

	random = SystemRandom()

	with open('flag.txt') as f:
		flag = f.read().strip().encode()

	key = [random.getrandbits(64) for _ in range(4)]

	simon68 = Simon(key, 68) # secure
	simon69 = Simon(key, 69) # super secure
	simon72 = Simon(key, 72) # ultra secure

	pt = flag + bytes(-len(flag) % 16)

	print(encrypt(simon68, pt).hex())
	print(encrypt(simon69, pt).hex())
	print(encrypt(simon72, pt).hex())
