import numpy as np
from hashlib import sha256
from Crypto.Random import random
import sys
import json

from secret import flag

class OverheatingError(Exception):
	pass

# PARAMS
n = 256
TRIGGER_CHANCE = 0.95
MAX_HEAT = 256

# CODE

def random_vector(a,b,n):
	return np.array([random.randrange(a,b+1) for _ in range(n)], dtype = np.int32)

class ILWE(object):
	"""Instance for the integer-LWE engine."""

	def __init__(self, n, seed = None):
		self.n = n
		self.heat_level = 0
		self.s = random_vector(-2,2,n)

	def measure(self):
		if self.heat_level >= MAX_HEAT:
			raise OverheatingError
		a = random_vector(-1,1,n)
		y = a @ self.s
		if np.random.rand() < 1 / (MAX_HEAT - self.heat_level) + 0.03:
			y += random.randrange(-16,16)
		if np.random.rand() < TRIGGER_CHANCE:
			self.heat_level += 1
			if self.heat_level == MAX_HEAT:
				print('Critical heat level reached')
		return a,y

	def verify(self,hash_value):
		return hash_value == sha256(self.s).hexdigest()

def loop():
	inst = ILWE(n)
	print('Getting new device...')
	while True:
		print('1) measure device\n2) provide secret')
		sys.stdout.flush()
		option = int(sys.stdin.buffer.readline().strip())
		if option == 1:
			a,y = inst.measure()
			print(json.dumps({'a':a.tolist(), 'y':int(y)}))
		elif option == 2:
			print('Please provide sha256 of the secret in hex:')
			hash_value = sys.stdin.buffer.readline().strip().decode()
			if inst.verify(hash_value):
				print(flag)
			else:
				raise Exception('Impostor! The correct value was %s' % sha256(inst.s).hexdigest())
		else:
			print('invalid option')

if __name__ == '__main__':
	try:
		loop()
	except Exception as err:
		print(repr(err))
		sys.stdout.flush()
