#!/usr/bin/env python3

from qiskit import QuantumCircuit, Aer
from numpy.random import randint
from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os
import hashlib

def encode_message(bits, bases):
	message = []
	for i in range(n):
		qc = QuantumCircuit(1,1)
		if bases[i] == 0: 
			if bits[i] == 0:
				pass 
			else:
				qc.x(0)
		else:
			if bits[i] == 0:
				qc.h(0)
			else:
				qc.x(0)
				qc.h(0)
		qc.barrier()
		message.append(qc)
	return message

def measure_message(message, bases):
	measurements = []
	for q in range(min(n,len(bases))):
		if bases[q] == 0: 
			message[q].measure(0,0)
		if bases[q] == 1: 
			message[q].h(0)
			message[q].measure(0,0)
		aer_sim = Aer.get_backend('aer_simulator')
		result = aer_sim.run(message[q], shots=1, memory=True).result()
		measured_bit = int(result.get_memory()[0])
		measurements.append(measured_bit)
	return measurements

def remove_garbage(a_bases, b_bases, bits):
	good_bits = []
	for q in range(n):
		if a_bases[q] == b_bases[q]:
			good_bits.append(bits[q])
	return good_bits

def verifyInput(lst):
	for i in lst:
		if i != 0 and i != 1:
			return False
	return True

n = 100

alice_bits = randint(2,size=n)
alice_bases = randint(2, size=n)
bob_bases = randint(2, size=n)

message = encode_message(alice_bits, alice_bases)
bob_results = measure_message(message, bob_bases)
alice_key = remove_garbage(alice_bases, bob_bases, alice_bits)
bob_key = remove_garbage(alice_bases, bob_bases, bob_results)
assert alice_key == bob_key

flag = pad(open('flag.txt','rb').read(),16)
key = hashlib.sha256(''.join([str(i) for i in alice_key]).encode()).digest()[:16]
iv = os.urandom(16)
cipher = AES.new(key=key, iv=iv, mode=AES.MODE_CBC)
enc = cipher.encrypt(flag)
print(f'iv = {iv.hex()}')
print(f'enc = {enc.hex()}')

while True:
	message = encode_message(alice_bits, alice_bases)
	
	eve_bases = [int(i) for i in input("Enter bases to intercept: ")]
	assert verifyInput(eve_bases)

	eve_results = measure_message(message, eve_bases)
	print("Measured message:", eve_results)
	
	new_bits = [int(i) for i in input("Enter bits to send to Bob: ")]
	assert verifyInput(new_bits)
	new_bits += alice_bits.tolist()[len(new_bits):]
	
	new_message = encode_message(new_bits, alice_bases)
	bob_results = measure_message(new_message, bob_bases)
	
	alice_key = remove_garbage(alice_bases, bob_bases, alice_bits)
	bob_key = remove_garbage(alice_bases, bob_bases, bob_results)
	print(alice_key == bob_key)
