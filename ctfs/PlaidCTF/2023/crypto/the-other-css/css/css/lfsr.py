class LFSR:
	size: int
	seed: int
	state: int
	taps: list[int]

	def __init__(self, size: int, seed: int, taps: int):
		self.size = size
		self.seed = seed
		self.state = seed

		assert taps < 2 ** size
		self.taps = []
		for i in range(size):
			tap = taps & (1 << i)
			if tap > 0:
				self.taps.append(tap)
		assert sum(self.taps) == taps, f'{self.taps=}, {taps=}, {sum(self.taps)=}'

	def next_bit(self) -> int:
		bit = 0
		for tap in self.taps:
			bit ^= (self.state & tap) == tap
		self.state = (self.state >> 1) | (bit << (self.size - 1))
		return bit

	def next_byte(self) -> int:
		byte = 0
		for i in range(8):
			byte |= self.next_bit() << i
		return byte
