from random import Random
from flag import flag
import string
import copy

class PRNG(Random):
	stream = ""
	prev = -1
	def __init__(self):
                super().__init__()

	def us(self):
		self.stream += bin(super().getrandbits(32))[2:].rjust(32, "0")

	def n(self, check=False):
		if check:
			bound = 12
		else:
			bound = 18
		if len(self.stream) < 32:
			self.us()
		nbits = bound.bit_length()
		res = int(self.stream[:nbits], 2) % bound
		if check:
			res = (((self.prev)//6+1)*6 + res)%18
		self.stream = self.stream[nbits:]
		assert self.prev != -1 or check == False
		self.prev = res
		return res

	def g(self, l=10):
		res = []
		for i in range(l):
			res.append(self.n(i!=0))
		return res

def cubify(a: str):
	return [[list(b[i:i+3]) for i in range(0, len(b), 3)] for b in [a[i:i+9] for i in range(0, len(a), 9)]]

def linify(a: list):
	return ''.join([''.join([''.join(c) for c in b]) for b in a])

def U_Turn(cube):
	tmp = cube[1][0]
	cube[1][0] = cube[2][0]
	cube[2][0] = cube[3][0]
	cube[3][0] = cube[4][0]
	cube[4][0] = tmp
	tmp = cube[0][0][0]
	cube[0][0][0] = cube[0][2][0]
	cube[0][2][0] = cube[0][2][2]
	cube[0][2][2] = cube[0][0][2]
	cube[0][0][2] = tmp
	tmp = cube[0][0][1]
	cube[0][0][1] = cube[0][1][0]
	cube[0][1][0] = cube[0][2][1]
	cube[0][2][1] = cube[0][1][2]
	cube[0][1][2] = tmp

def U_Turn_Prime(cube):
	tmp = cube[1][0]
	cube[1][0] = cube[4][0]
	cube[4][0] = cube[3][0]
	cube[3][0] = cube[2][0]
	cube[2][0] = tmp
	tmp = cube[0][0][0]
	cube[0][0][0] = cube[0][0][2]
	cube[0][0][2] = cube[0][2][2]
	cube[0][2][2] = cube[0][2][0]
	cube[0][2][0] = tmp
	tmp = cube[0][0][1]
	cube[0][0][1] = cube[0][1][2]
	cube[0][1][2] = cube[0][2][1]
	cube[0][2][1] = cube[0][1][0]
	cube[0][1][0] = tmp

def L_Turn(cube):
	tmp = [cube[2][0][0], cube[2][1][0], cube[2][2][0]]
	cube[2][0][0] = cube[0][0][0]
	cube[2][1][0] = cube[0][1][0]
	cube[2][2][0] = cube[0][2][0]
	cube[0][0][0] = cube[4][2][2]
	cube[0][1][0] = cube[4][1][2]
	cube[0][2][0] = cube[4][0][2]
	cube[4][0][2] = cube[5][2][0]
	cube[4][1][2] = cube[5][1][0]
	cube[4][2][2] = cube[5][0][0]
	cube[5][0][0] = tmp[0]
	cube[5][1][0] = tmp[1]
	cube[5][2][0] = tmp[2]
	tmp = cube[1][0][0]
	cube[1][0][0] = cube[1][2][0]
	cube[1][2][0] = cube[1][2][2]
	cube[1][2][2] = cube[1][0][2]
	cube[1][0][2] = tmp
	tmp = cube[1][0][1]
	cube[1][0][1] = cube[1][1][0]
	cube[1][1][0] = cube[1][2][1]
	cube[1][2][1] = cube[1][1][2]
	cube[1][1][2] = tmp

def L_Turn_Prime(cube):
	tmp = [cube[4][2][2], cube[4][1][2], cube[4][0][2]]
	cube[4][0][2] = cube[0][2][0]
	cube[4][1][2] = cube[0][1][0]
	cube[4][2][2] = cube[0][0][0]
	cube[0][0][0] = cube[2][0][0]
	cube[0][1][0] = cube[2][1][0]
	cube[0][2][0] = cube[2][2][0]
	cube[2][0][0] = cube[5][0][0]
	cube[2][1][0] = cube[5][1][0]
	cube[2][2][0] = cube[5][2][0]
	cube[5][0][0] = tmp[0]
	cube[5][1][0] = tmp[1]
	cube[5][2][0] = tmp[2]
	tmp = cube[1][0][0]
	cube[1][0][0] = cube[1][0][2]
	cube[1][0][2] = cube[1][2][2]
	cube[1][2][2] = cube[1][2][0]
	cube[1][2][0] = tmp
	tmp = cube[1][0][1]
	cube[1][0][1] = cube[1][1][2]
	cube[1][1][2] = cube[1][2][1]
	cube[1][2][1] = cube[1][1][0]
	cube[1][1][0] = tmp

def F_Turn(cube):
	tmp = [cube[0][2][0], cube[0][2][1], cube[0][2][2]]
	cube[0][2][0] = cube[1][2][2]
	cube[0][2][1] = cube[1][1][2]
	cube[0][2][2] = cube[1][0][2]
	cube[1][2][2] = cube[5][0][2]
	cube[1][1][2] = cube[5][0][1]
	cube[1][0][2] = cube[5][0][0]
	cube[5][0][2] = cube[3][0][0]
	cube[5][0][1] = cube[3][1][0]
	cube[5][0][0] = cube[3][2][0]
	cube[3][0][0] = tmp[0]
	cube[3][1][0] = tmp[1]
	cube[3][2][0] = tmp[2]
	tmp = cube[2][0][0]
	cube[2][0][0] = cube[2][2][0]
	cube[2][2][0] = cube[2][2][2]
	cube[2][2][2] = cube[2][0][2]
	cube[2][0][2] = tmp
	tmp = cube[2][0][1]
	cube[2][0][1] = cube[2][1][0]
	cube[2][1][0] = cube[2][2][1]
	cube[2][2][1] = cube[2][1][2]
	cube[2][1][2] = tmp

def F_Turn_Prime(cube):
	tmp = [cube[3][0][0], cube[3][1][0], cube[3][2][0]]
	cube[3][0][0] = cube[5][0][2]
	cube[3][1][0] = cube[5][0][1]
	cube[3][2][0] = cube[5][0][0]
	cube[5][0][2] = cube[1][2][2]
	cube[5][0][1] = cube[1][1][2]
	cube[5][0][0] = cube[1][0][2]
	cube[1][2][2] = cube[0][2][0]
	cube[1][1][2] = cube[0][2][1]
	cube[1][0][2] = cube[0][2][2]
	cube[0][2][0] = tmp[0]
	cube[0][2][1] = tmp[1]
	cube[0][2][2] = tmp[2]
	tmp = cube[2][0][0]
	cube[2][0][0] = cube[2][0][2]
	cube[2][0][2] = cube[2][2][2]
	cube[2][2][2] = cube[2][2][0]
	cube[2][2][0] = tmp
	tmp = cube[2][0][1]
	cube[2][0][1] = cube[2][1][2]
	cube[2][1][2] = cube[2][2][1]
	cube[2][2][1] = cube[2][1][0]
	cube[2][1][0] = tmp

def R_Turn(cube):
	tmp = [cube[5][0][2], cube[5][1][2], cube[5][2][2]]
	cube[5][0][2] = cube[4][2][0]
	cube[5][1][2] = cube[4][1][0]
	cube[5][2][2] = cube[4][0][0]
	cube[4][0][0] = cube[0][2][2]
	cube[4][1][0] = cube[0][1][2]
	cube[4][2][0] = cube[0][0][2]
	cube[0][0][2] = cube[2][0][2]
	cube[0][1][2] = cube[2][1][2]
	cube[0][2][2] = cube[2][2][2]
	cube[2][0][2] = tmp[0]
	cube[2][1][2] = tmp[1]
	cube[2][2][2] = tmp[2]
	tmp = cube[3][0][0]
	cube[3][0][0] = cube[3][2][0]
	cube[3][2][0] = cube[3][2][2]
	cube[3][2][2] = cube[3][0][2]
	cube[3][0][2] = tmp
	tmp = cube[3][0][1]
	cube[3][0][1] = cube[3][1][0]
	cube[3][1][0] = cube[3][2][1]
	cube[3][2][1] = cube[3][1][2]
	cube[3][1][2] = tmp

def R_Turn_Prime(cube):
	tmp = [cube[2][0][2], cube[2][1][2], cube[2][2][2]]
	cube[2][0][2] = cube[0][0][2]
	cube[2][1][2] = cube[0][1][2]
	cube[2][2][2] = cube[0][2][2]
	cube[0][2][2] = cube[4][0][0]
	cube[0][1][2] = cube[4][1][0]
	cube[0][0][2] = cube[4][2][0]
	cube[4][2][0] = cube[5][0][2]
	cube[4][1][0] = cube[5][1][2]
	cube[4][0][0] = cube[5][2][2]
	cube[5][0][2] = tmp[0]
	cube[5][1][2] = tmp[1]
	cube[5][2][2] = tmp[2]
	tmp = cube[3][0][0]
	cube[3][0][0] = cube[3][0][2]
	cube[3][0][2] = cube[3][2][2]
	cube[3][2][2] = cube[3][2][0]
	cube[3][2][0] = tmp
	tmp = cube[3][0][1]
	cube[3][0][1] = cube[3][1][2]
	cube[3][1][2] = cube[3][2][1]
	cube[3][2][1] = cube[3][1][0]
	cube[3][1][0] = tmp

def B_Turn(cube):
	tmp = [cube[0][0][2], cube[0][0][1], cube[0][0][0]]
	cube[0][0][0] = cube[3][0][2]
	cube[0][0][1] = cube[3][1][2]
	cube[0][0][2] = cube[3][2][2]
	cube[3][0][2] = cube[5][2][2]
	cube[3][1][2] = cube[5][2][1]
	cube[3][2][2] = cube[5][2][0]
	cube[5][2][0] = cube[1][0][0]
	cube[5][2][1] = cube[1][1][0]
	cube[5][2][2] = cube[1][2][0]
	cube[1][0][0] = tmp[0]
	cube[1][1][0] = tmp[1]
	cube[1][2][0] = tmp[2]
	tmp = cube[4][0][0]
	cube[4][0][0] = cube[4][2][0]
	cube[4][2][0] = cube[4][2][2]
	cube[4][2][2] = cube[4][0][2]
	cube[4][0][2] = tmp
	tmp = cube[4][0][1]
	cube[4][0][1] = cube[4][1][0]
	cube[4][1][0] = cube[4][2][1]
	cube[4][2][1] = cube[4][1][2]
	cube[4][1][2] = tmp

def B_Turn_Prime(cube):
	tmp = [cube[1][0][0], cube[1][1][0], cube[1][2][0]]
	cube[1][0][0] = cube[5][2][0]
	cube[1][1][0] = cube[5][2][1]
	cube[1][2][0] = cube[5][2][2]
	cube[5][2][2] = cube[3][0][2]
	cube[5][2][1] = cube[3][1][2]
	cube[5][2][0] = cube[3][2][2]
	cube[3][0][2] = cube[0][0][0]
	cube[3][1][2] = cube[0][0][1]
	cube[3][2][2] = cube[0][0][2]
	cube[0][0][2] = tmp[0]
	cube[0][0][1] = tmp[1]
	cube[0][0][0] = tmp[2]
	tmp = cube[4][0][0]
	cube[4][0][0] = cube[4][0][2]
	cube[4][0][2] = cube[4][2][2]
	cube[4][2][2] = cube[4][2][0]
	cube[4][2][0] = tmp
	tmp = cube[4][0][1]
	cube[4][0][1] = cube[4][1][2]
	cube[4][1][2] = cube[4][2][1]
	cube[4][2][1] = cube[4][1][0]
	cube[4][1][0] = tmp

def D_Turn(cube):
	tmp = [cube[3][2][0], cube[3][2][1], cube[3][2][2]]
	cube[3][2][0] = cube[2][2][0]
	cube[3][2][1] = cube[2][2][1]
	cube[3][2][2] = cube[2][2][2]
	cube[2][2][0] = cube[1][2][0]
	cube[2][2][1] = cube[1][2][1]
	cube[2][2][2] = cube[1][2][2]
	cube[1][2][0] = cube[4][2][0]
	cube[1][2][1] = cube[4][2][1]
	cube[1][2][2] = cube[4][2][2]
	cube[4][2][0] = tmp[0]
	cube[4][2][1] = tmp[1]
	cube[4][2][2] = tmp[2]
	tmp = cube[5][0][0]
	cube[5][0][0] = cube[5][2][0]
	cube[5][2][0] = cube[5][2][2]
	cube[5][2][2] = cube[5][0][2]
	cube[5][0][2] = tmp
	tmp = cube[5][0][1]
	cube[5][0][1] = cube[5][1][0]
	cube[5][1][0] = cube[5][2][1]
	cube[5][2][1] = cube[5][1][2]
	cube[5][1][2] = tmp

def D_Turn_Prime(cube):
	tmp = [cube[4][2][0], cube[4][2][1], cube[4][2][2]]
	cube[4][2][0] = cube[1][2][0]
	cube[4][2][1] = cube[1][2][1]
	cube[4][2][2] = cube[1][2][2]
	cube[1][2][0] = cube[2][2][0]
	cube[1][2][1] = cube[2][2][1]
	cube[1][2][2] = cube[2][2][2]
	cube[2][2][0] = cube[3][2][0]
	cube[2][2][1] = cube[3][2][1]
	cube[2][2][2] = cube[3][2][2]
	cube[3][2][0] = tmp[0]
	cube[3][2][1] = tmp[1]
	cube[3][2][2] = tmp[2]
	tmp = cube[5][0][0]
	cube[5][0][0] = cube[5][0][2]
	cube[5][0][2] = cube[5][2][2]
	cube[5][2][2] = cube[5][2][0]
	cube[5][2][0] = tmp
	tmp = cube[5][0][1]
	cube[5][0][1] = cube[5][1][2]
	cube[5][1][2] = cube[5][2][1]
	cube[5][2][1] = cube[5][1][0]
	cube[5][1][0] = tmp

def call_algorithm(cube: list, algorithm: list):
	for move in algorithm:
		caller[move](cube)

caller = {
	0: U_Turn,
	1: lambda cb: (U_Turn(cb), U_Turn(cb)),
	2: U_Turn_Prime,
	3: D_Turn,
	4: lambda cb: (D_Turn(cb), D_Turn(cb)),
	5: D_Turn_Prime,
	6: L_Turn,
	7: lambda cb: (L_Turn(cb), L_Turn(cb)),
	8: L_Turn_Prime,
	9: R_Turn,
	10: lambda cb: (R_Turn(cb), R_Turn(cb)),
	11: R_Turn_Prime,
	12: F_Turn,
	13: lambda cb: (F_Turn(cb), F_Turn(cb)),
	14: F_Turn_Prime,
	15: B_Turn,
	16: lambda cb: (B_Turn(cb), B_Turn(cb)),
	17: B_Turn_Prime
}

if __name__ == '__main__':
	assert flag[:7] == "LITCTF{"
	assert flag[-1] == "}"
	flag = flag[7:-1]
	assert len(flag) == 54
	og = string.ascii_letters + "01"
	cube = cubify(og)

	reserve = copy.deepcopy(cube)
	prng = PRNG()
	while True:
		a=input("")
		if a=="1":
			cube = copy.deepcopy(reserve)
			moves = prng.g()
			call_algorithm(cube, moves)
			print(linify(cube))
		elif a=="2":
			cube = cubify(flag)
			moves = prng.g(100)
			call_algorithm(cube, moves)
			print(linify(cube))
			exit(0)
		else:
			exit(0)
