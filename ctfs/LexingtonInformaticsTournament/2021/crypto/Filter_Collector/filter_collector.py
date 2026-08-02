#!/usr/bin/python3
from Crypto.Util.number import getPrime
import random
import math
import cmath

Welcome = "Instagram filters are fun, aren't they?"
print(Welcome);

flag = int(open('flag.txt','rb').read().hex(),16);
k = 7
p = int(input("Input your favorite mod: "));
assert(p * p < flag);

# Divides tot randomly into n parts
def get_partition(tot,n):
	partitions = [tot];
	for i in range(n - 1):
		partitions.append(random.randint(0,tot));
	partitions.sort()
	for i in range(n - 1,0,-1):
		partitions[i] -= partitions[i - 1];
	return partitions

def gen_poly(partitions,n):
	poly = [];
	cnt = 0
	for i in range(n):
		if(i % k == 0):
			poly.append(partitions[cnt]);
			cnt += 1;
		else:
			poly.append(random.randint(0,p - 1));
	assert(cnt == len(partitions));
	return poly

def hash(poly,x):
	res = 0;
	for i,c in enumerate(poly):
		res += c * pow(x,i,p) % p;
	return res % p;

partitions = get_partition(flag,(199 // k) + 1);
poly = gen_poly(partitions,200);
for i in range(k):
	x = int(input("Input the a number: "));
	y = hash(poly,x);
	print("The hash of the number under your mod filter is " + str(y));