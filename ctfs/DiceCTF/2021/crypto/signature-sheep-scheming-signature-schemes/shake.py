from random import Random, RECIP_BPF

from Crypto.Hash import SHAKE128
from Crypto.Util.number import bytes_to_long

class ShakeRandom(Random):

	def __init__(self, data):
		self.shake = SHAKE128.new(data)
		self.gauss_next = None

	def random(self):
		return (bytes_to_long(self.shake.read(7)) >> 3) * RECIP_BPF

	def getrandbits(self, k):
		return bytes_to_long(self.shake.read((k + 7) // 8)) >> (-k % 8)
