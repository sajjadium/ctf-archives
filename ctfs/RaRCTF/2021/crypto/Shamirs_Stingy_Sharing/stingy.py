import random, sys
from Crypto.Util.number import long_to_bytes

def bxor(ba1,ba2):
	return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

BITS = 128
SHARES = 30

poly = [random.getrandbits(BITS) for _ in range(SHARES)]
flag = open("/challenge/flag.txt","rb").read()

random.seed(poly[0])
print(bxor(flag, long_to_bytes(random.getrandbits(len(flag)*8))).hex())

try:
	x = int(input('Take a share... BUT ONLY ONE. '))
except:
	print('Do you know what an integer is?')
	sys.exit(1)
if abs(x) < 1:
	print('No.')
else:
	print(sum(map(lambda i: poly[i] * pow(x, i), range(len(poly)))))