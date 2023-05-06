#!/usr/bin/env python3
import random

def get_seed(l):
	seed = 0
	rand = random.getrandbits(l)
	raw = list()
	
	while rand > 0:
		rand = rand >> 1
		seed += rand
		raw.append(rand)
	
	if len(raw) == l:
		return raw, seed
	else:
		return get_seed(l)

def encrypt(m):
	l = len(m)

	raw, seed = get_seed(l)
	random.seed(seed)

	with open('encrypted.txt', 'w') as f:	
		for i in range(l):
			r = random.randint(1, 2**512)
			if i == 0:
				print("r0 =",r)
			encoded = hex(r ^ m[i] ^ raw[i])[2:]
			f.write(f"F{i}:  {encoded}\n")

def main():
	m = open('flag.txt').read()
	encrypt(m.encode())

if __name__=='__main__':
	main()
