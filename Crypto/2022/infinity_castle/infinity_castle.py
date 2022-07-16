#!/usr/bin/env python3

from Crypto.Util.number import *
from os import urandom

class TaylorSeries():

	def __init__(self, order):
		self.order = order
		
	def coefficient(self, n):
		i = 0
		coef = 1
		while i < n:
			i += 1
			coef *= (coef * (1/2-i+1)) / i
		return coef

	def find(self, center):
		sum = 0
		center -= 1
		i = 0
		while i < self.order:
			sum += (center**(1/2-i) * self.coefficient(i))
			i += 1
		return sum

def xor(cip, key):
	repeation = 1 + (len(cip) // len(key))
	key = key * repeation
	key = key[:len(cip)]
	
	msg = bytes([c ^ k for c, k in zip(cip, key)])
	return msg

# If you run these 3 functions (diamond, triage, summarize) with big numbers, they will never end
# You need to optimize them first

def diamond(num):
	output = 0
	for i in range(num):
		output += i*2 + 1
	return output

def triage(num):
	output = 0
	index = 0
	for i in range(num):
		output += (i+index)*6 + 1
		index += i
	return output

def summarize(b):
	order = getRandomRange(1000, 2000)
	t = TaylorSeries(order)
	output = 0
	
	i = 2
	while i < b:
		b1 = t.find(i)
		b2 = t.find(i+1)
		output += (b1+b2) / 2
		i += 1
	return output

KEY_SIZE = 2048
p, q = [getPrime(KEY_SIZE) for _ in '01']

e, n = 0x10001, p*q

f = open ('./message.txt', 'rb')
message = f.read()
f.close()
msg_length = len(message)
padded_msg = message + urandom(len(long_to_bytes(n)) - msg_length)
padded_msg_length = len(padded_msg)

xor_key = long_to_bytes(int(summarize(n)))[:padded_msg_length]
assert(len(xor_key) == 512)

enc0 = xor(padded_msg, xor_key)
assert(bytes_to_long(enc0) < n)

c0 =  abs(diamond(p) - diamond(q))
c1 =  triage(p)
c1 += 3*n*(p+q)
c1 += triage(q)

m = bytes_to_long(enc0)
enc1 = pow(m, e, n)

print(f"c0 = {c0}")
print(f"c1 = {c1}")
print(f"enc = {enc1}")