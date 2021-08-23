import numpy as np
import math, random

flag = open('flag.txt').read()

class Qubit:
	def __init__(self, vector):
		self.vec = vector

	def x(self):
		mat = np.array([[0, 1], [1, 0]])
		self.vec = mat.dot(self.vec)

	def y(self):
		mat = np.array([[0, -1j], [1j, 0]])
		self.vec = mat.dot(self.vec)

	def z(self):
		mat = np.array([[1, 0], [0, -1]])
		self.vec = mat.dot(self.vec)

	def h(self):
		mat = np.array([[1/math.sqrt(2), 1/math.sqrt(2)], [1/math.sqrt(2), -1/math.sqrt(2)]])
		self.vec = mat.dot(self.vec)

	def rotate(self, angle):
		mat = np.array([[1, 0], [0, np.exp(1j * angle)]])
		self.vec = mat.dot(self.vec)

	def measure(self, basis):
		if basis == '01':
			if random.random() < np.linalg.norm(self.vec[0]) ** 2:
				self.vec = np.array([[1], [0]])
				return '0'
			else:
				self.vec = np.array([[0], [1]])
				return '1'
		elif basis == '+-':
			pvec = np.array([[1/math.sqrt(2)], [1/math.sqrt(2)]])
			prob = np.linalg.norm(self.vec.T.dot(pvec)) ** 2
			if random.random() < prob:
				self.vec = pvec
				return '+'
			else:
				self.vec = np.array([[1/math.sqrt(2)], [-1/math.sqrt(2)]])
				return '-'
		else:
			raise ValueError('Invalid basis to measure on')
	
	@staticmethod
	def from_str(symbol):
		if symbol == '0':
			return Qubit(np.array([[1], [0]]))
		elif symbol == '1':
			return Qubit(np.array([[0], [1]]))
		elif symbol == '+':
			return Qubit(np.array([[1/math.sqrt(2)], [1/math.sqrt(2)]]))
		elif symbol == '-':
			return Qubit(np.array([[1/math.sqrt(2)], [-1/math.sqrt(2)]]))
		raise ValueError('Invalid symbol to construct qubit with')

print('Welcome to the CoR bank!')
print("We're currently running a special promotion where new accounts receive one free dollar. Terms and conditions apply.")
choice = input('Would you like an account? (y/n) ')

if choice.lower() == 'n':
	print('Well what did you connect for? Stop wasting my time')
	exit()
elif choice.lower() != 'y':
	print('Bruh')
	exit()

symbols = ['0', '1', '+', '-']
bill = [random.choice(symbols) for _ in range(50)]
qubits = [Qubit.from_str(s) for s in bill]

print('New account made! Enjoy your $1.')
print()

while True:
	print('What would you like to do with your account?')
	print()
	print('1. Work with qubits')
	print('2. Buy flag')
	print('3. Quit')

	choice = input('> ')
	if choice == '1':
		idx = int(input('Please input the index of the qubit you wish to work with: '))
		while True:
			print('What operation would you like to perform?')
			print()
			print('1. Apply X gate')
			print('2. Apply Y gate')
			print('3. Apply Z gate')
			print('4. Apply Hadamard gate')
			print('5. Apply rotation gate')
			print('6. Measure qubit in 0/1 basis')
			print('7. Measure qubit in +/- basis')
			print('8. Verify qubit')
			print('9. Back')
			op = input('> ')
			if op == '1':
				qubits[idx].x()
			elif op == '2':
				qubits[idx].y()
			elif op == '3':
				qubits[idx].z()
			elif op == '4':
				qubits[idx].h()
			elif op == '5':
				angle = float(input('Input angle to rotate by (in radians): '))
				if np.isnan(angle) or np.isinf(angle):
					print('Pepega')
				else:
					qubits[idx].rotate(angle)
			elif op == '6':
				print('The qubit measured as', qubits[idx].measure('01'))
			elif op == '7':
				print('The qubit measured as', qubits[idx].measure('+-'))
			elif op == '8':
				actual = bill[idx]
				if actual in '01':
					measured = qubits[idx].measure('01')
				else:
					measured = qubits[idx].measure('+-')
				if actual == measured:
					print('Qubit successfully verified.')
				else:
					print('Incorrect qubit!')
			elif op == '9':
				break
			else:
				print('Invalid operation.')
				exit()
	elif choice == '2':
		print('Flags cost $1.')
		qstr = input('Enter your bill: ')
		if qstr == ''.join(bill):
			print('Congratulations!', flag)
		else:
			print('Are you trying to scam me?')
			exit()
	else:
		print('Cya')
		exit()
