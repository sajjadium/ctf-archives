import secrets
from sympy import N, Float, Point, Triangle

from secret import FLAG

PRECISION = 1337

def main():
	import signal
	signal.alarm(20)

	levels = [
		lambda x: x.centroid,
		lambda x: x.circumcenter,
		lambda x: x.incenter,
	]
	try:
		for level in levels:
			challenge(level)
		print(FLAG)
	except:
		print("Wasted")

def challenge(hash_function):
	# raise an error if the user fails the challenge

	print("===== Challenge =====")
	A = RandomLine()
	B = RandomLine()
	C = RandomLine()

	# print parameters
	A.print()
	B.print()
	C.print()

	i, j, k = [secrets.randbits(32) for _ in range(3)]
	triangle = Triangle(A[i], B[j], C[k])
	hsh = hash_function(triangle)
	
	print(Float(hsh.x, PRECISION))
	print(Float(hsh.y, PRECISION))

	_i, _j, _k = map(int, input("> ").split(" "))
	assert (i, j, k) == (_i, _j, _k)
	print("Mission passed")

class RandomLine:
	def __init__(self):
		self.x = randFloat()
		self.y = randFloat()
		self.dx = randFloat()
		self.dy = randFloat()

	def __getitem__(self, i):
		return Point(self.x + self.dx * i, self.y + self.dy * i, evaluate=False)

	def print(self):
		print(self.x)
		print(self.y)
		print(self.dx)
		print(self.dy)

def randFloat():
	# return a random float between -1 and 1
	return -1 + 2 * Float(secrets.randbits(PRECISION), PRECISION) / (1 << PRECISION)

if __name__ == "__main__":
	main()