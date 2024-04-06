#!/bin/python3

from Crypto.Util.number import *

with open('flag.txt', 'rb') as fin:
	flag = fin.read().rstrip()

pad = lambda x: x + b'\x00' * (500 - len(x))

m = bytes_to_long(pad(flag))

p = getStrongPrime(512)
q = getStrongPrime(512)

n = p * q
e = 3
c = pow(m,e,n)

with open('out.txt', 'w') as fout:
	fout.write(f'n = {n}\n')
	fout.write(f'e = {e}\n')
	fout.write(f'c = {c}\n')
