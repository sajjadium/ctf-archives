import random;
import math;

flag = int(open('flag.txt','rb').read().hex(),16);

class MiseryStraightener:
	def __init__(self):
		random.seed(1337);

		self.bits = 42;
		self.pool = [random.getrandbits(self.bits) for _ in range(13)];
		self.randomConstant = random.getrandbits(self.bits);

	def next(self):
		res = self.pool[-1];
		a = self.pool[12];
		b = self.pool[6];
		c = a ^ b;
		c = c ^ (a >> 10);
		c = c ^ ((b % (1 << 20)) << (self.bits - 20));
		d = (1 << self.bits) - 1 - c;
		e = d;
		if(self.pool[8] & 8):
			e ^= self.randomConstant;

		self.pool.pop();
		self.pool.insert(0,e);
		return res;

	def fastforward(self,x):
		for i in range(x):
			self.next();
		return;



generator = MiseryStraightener();
generator.fastforward(int(1e18));
for i in range(10):
	flag ^= generator.next() << (i * generator.bits);
	
print(flag);

# Outputs
# 961324187529262150231144941297949459498043797601643810714360754627060734634014359407613152643271495586117006168448502325284326