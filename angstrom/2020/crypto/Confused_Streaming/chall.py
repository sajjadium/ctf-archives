from __future__ import print_function
import random,os,sys,binascii
from decimal import *
try:
	input = raw_input
except:
	pass
getcontext().prec = 1000
def keystream(key):
	random.seed(int(os.environ["seed"]))
	e = random.randint(100,1000)
	while 1:
		d = random.randint(1,100)
		ret = Decimal('0.'+str(key ** e).split('.')[-1])
		for i in range(d):
			ret*=2
		yield int((ret//1)%2)
		e+=1
try:
	a = int(input("a: "))
	b = int(input("b: "))
	c = int(input("c: "))
	# remove those pesky imaginary numbers, rationals, zeroes, integers, big numbers, etc
	if b*b < 4*a*c or a==0 or b==0 or c==0 or Decimal(b*b-4*a*c).sqrt().to_integral_value()**2==b*b-4*a*c or abs(a)>1000 or abs(b)>1000 or abs(c)>1000:
		raise Exception()
	key = (Decimal(b*b-4*a*c).sqrt() - Decimal(b))/Decimal(a*2)
except:
	print("bad key")
else:
	flag = binascii.hexlify(os.environ["flag"].encode())
	flag = bin(int(flag,16))[2:].zfill(len(flag)*4)
	ret = ""
	k = keystream(key)
	for i in flag:
		ret += str(next(k)^int(i))
	print(ret)