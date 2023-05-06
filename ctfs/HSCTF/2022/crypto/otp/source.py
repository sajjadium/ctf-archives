import random
from Crypto.Util.number import bytes_to_long

def secure_seed():
	x = 0
	# x is a random integer between 0 and 100000000000
	for i in range(10000000000):
		x += random.randint(0, random.randint(0, 10))
	return x

flag = open('flag.txt','rb').read()
flag = bytes_to_long(flag)

random.seed(secure_seed())

l = len(bin(flag)) - 1
print(l)

k = random.getrandbits(l)
flag = flag ^ k # super secure encryption
print(flag)

