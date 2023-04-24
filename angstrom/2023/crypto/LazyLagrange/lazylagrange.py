#!/usr/local/bin/python
import random

with open('flag.txt', 'r') as f:
	FLAG = f.read()

assert all(c.isascii() and c.isprintable() for c in FLAG), 'Malformed flag'
N = len(FLAG)
assert N <= 18, 'I\'m too lazy to store a flag that long.'
p = None
a = None
M = (1 << 127) - 1

def query1(s):
	if len(s) > 100:
		return 'I\'m too lazy to read a query that long.'
	x = s.split()
	if len(x) > 10:
		return 'I\'m too lazy to process that many inputs.'
	if any(not x_i.isdecimal() for x_i in x):
		return 'I\'m too lazy to decipher strange inputs.'
	x = (int(x_i) for x_i in x)
	global p, a
	p = random.sample(range(N), k=N)
	a = [ord(FLAG[p[i]]) for i in range(N)]
	res = ''
	for x_i in x:
		res += f'{sum(a[j] * x_i ** j for j in range(N)) % M}\n'
	return res

query1('0')

def query2(s):
	if len(s) > 100:
		return 'I\'m too lazy to read a query that long.'
	x = s.split()
	if any(not x_i.isdecimal() for x_i in x):
		return 'I\'m too lazy to decipher strange inputs.'
	x = [int(x_i) for x_i in x]
	while len(x) < N:
		x.append(0)
	z = 1
	for i in range(N):
		z *= not x[i] - a[i]
	return ' '.join(str(p_i * z) for p_i in p)

while True:
	try:
		choice = int(input(": "))
		assert 1 <= choice <= 2
		match choice:
			case 1:
				print(query1(input("\t> ")))
			case 2:
				print(query2(input("\t> ")))
	except Exception as e:
		print("Bad input, exiting", e)
		break