#!/usr/bin/env python3

import random
import math

secret = #REDACTED
flag = #REDACTED

def keygen(n):
	privKey = [0]*n
	privKey[0] = #REDACTED
	for i in range(1, n):
		total = sum(privKey)
		privKey[i] = random.randint(total*2 ,total*3) 

	privKey = tuple(privKey)
	total = sum(privKey)
	modulo = random.randint(total*2 ,total*3)

	while True:
		multiplier = random.randint(modulo//4, modulo-1)
		if math.gcd(multiplier, modulo):
			break

	pubKey = [multiplier*privKey[i]%modulo for i in range(n)]

	return pubKey

def encryption(enc_state):
	global pubKey
	pubKey = keygen(n=32)
	enc_array = []

	for i in state_one:
		result = 0
		j= bin(i)[2:].zfill(32)
		for k,b in zip(j, pubKey):
			result+=(int(k)*b)
		enc_array.append(result)

	return(tuple(enc_array))


random.seed(secret)

state = random.getstate()

enc_flag = 0
state_one = state[1]

random_number = random.randint(1, 2**8)

shuffled_flag = (''.join(random.sample(flag,len(flag))))


for i in shuffled_flag:
	enc_flag=(enc_flag*(random_number**ord(i)))+ord(i)

enc_state_one = encryption(state_one)
enc_state = tuple([state[0], enc_state_one, state[2]])

print(enc_flag)
print(enc_state)
print(pubKey)

