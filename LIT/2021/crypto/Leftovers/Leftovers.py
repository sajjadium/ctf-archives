import random
import binascii
import math
import sympy

random.seed(1337)

class PRNG:
	def __init__(self,seed):
		self.seed = seed;
		self.L = 1;

	# Returns a random number between [0,x)
	def rand(self,x):
		return self.seed % sympy.prevprime(x);

def str2Dec(str):
	return int(binascii.hexlify(str.encode("utf-8")),16);

flag = open('flag.txt','rb').read().decode("utf-8");
ct = str2Dec(flag);

NUMBER_OF_DIGITS = 128;
assert(math.log10(ct) <= 128)

g = PRNG(ct);
res = [];

for i in range(12):
	x = random.randint(1,4e10);
	res.append(g.rand(x));

print(res);
