#!/usr/local/bin/python

from collections import namedtuple
from Crypto.Hash import SHAKE128
from Crypto.Random import get_random_bytes, random
from Crypto.Util.strxor import strxor

def get_truth_table(op):
	match op:
		case 'and':
			return [
				[0, 0, 0],
				[0, 1, 0],
				[1, 0, 0],
				[1, 1, 1],
			]
		case 'xor':
			return [
				[0, 0, 0],
				[0, 1, 1],
				[1, 0, 1],
				[1, 1, 0],
			]

BUF_LEN = 16

def rand_bit():
	return random.getrandbits(1)

def rand_buf():
	return get_random_bytes(BUF_LEN)

class Wire:
	Label = namedtuple('Label', 'key ptr')

	def __init__(self, zero, one):
		self.zero = zero
		self.one = one

	@classmethod
	def new(cls):
		bit = rand_bit()
		zero = Wire.Label(rand_buf(), bit)
		one = Wire.Label(rand_buf(), bit ^ 1)
		return cls(zero, one)

	def get_label(self, value):
		match value:
			case 0:
				return self.zero
			case 1:
				return self.one
			case _:
				raise ValueError('cannot translate value to label')

	def get_value(self, label):
		match label:
			case self.zero:
				return 0
			case self.one:
				return 1
			case _:
				raise ValueError('cannot translate label to value')

class Cipher:
	def __init__(self, *labels):
		key = b''.join([l.key for l in labels])
		self.shake = SHAKE128.new(key)

	def xor_buf(self, buf):
		return strxor(buf, self.shake.read(BUF_LEN))	

	def xor_bit(self, bit):
		return bit ^ self.shake.read(1)[0] & 1

	def encrypt(self, label):
		return self.xor_buf(label.key), self.xor_bit(label.ptr)

	def decrypt(self, row):
		return Wire.Label(self.xor_buf(row[0]), self.xor_bit(row[1]))

def garble_gate(op, wa, wb):
	wc = Wire.new()
	table = [[None, None], [None, None]]
	for va, vb, vc in get_truth_table(op):
		la = wa.get_label(va)
		lb = wb.get_label(vb)
		lc = wc.get_label(vc)
		table[la.ptr][lb.ptr] = Cipher(la, lb).encrypt(lc)
	return wc, table

def evaluate_gate(table, la, lb):
	row = table[la.ptr][lb.ptr]
	return Cipher(la, lb).decrypt(row)

def garble(circuit):
	wires = []
	in_wires = []
	out_wires = []
	tables = []
	for line in circuit:
		match line:
			case ('id',):
				wire = Wire.new()
				wires.append(wire)
				in_wires.append(wire)
			case ('id', a):
				wires.append(None)
				out_wires.append(wires[a])
			case (op, a, b):
				wire, table = garble_gate(op, wires[a], wires[b])
				wires.append(wire)
				tables.append(table)
	return in_wires, out_wires, tables

def evaluate(circuit, in_labels, out_wires, tables):
	in_labels = iter(in_labels)
	out_wires = iter(out_wires)
	tables = iter(tables)
	labels = []
	out_bits = []
	for line in circuit:
		match line:
			case ('id',):
				labels.append(next(in_labels))
			case ('id', a):
				labels.append(None)
				out_bits.append(next(out_wires).get_value(labels[a]))
			case (_, a, b):
				labels.append(evaluate_gate(next(tables), labels[a], labels[b]))
	return out_bits

if __name__ == '__main__':
	from binteger import Bin

	with open('flag.txt', 'rb') as f:
		flag_bits = Bin(f.read().strip())

	print(f'Welcome to Snap Circuits: Garbled Edition! You have {len(flag_bits)} inputs to work with. Only AND and XOR gates are allowed, and no outputs.')

	circuit = [('id',) for _ in flag_bits]

	while True:
		gate = input('gate: ')
		tokens = gate.split(' ')
		try:
			assert len(tokens) == 3
			assert tokens[0] in ('and', 'xor')
			assert tokens[1].isdecimal()
			assert tokens[2].isdecimal()
			op = tokens[0]
			a = int(tokens[1])
			b = int(tokens[2])
			assert 0 <= a < len(circuit)
			assert 0 <= b < len(circuit)
			assert len(circuit) < 1000
			circuit.append((op, a, b))
		except:
			print('moving on...')
			break

	in_wires, _, tables = garble(circuit)

	for i, b in enumerate(flag_bits):
		label = in_wires[i].get_label(b)
		print(f'wire {i}: {label.key.hex()} {label.ptr}')

	print('table data:')
	for table in tables:
		for i in range(2):
			for j in range(2):
				row = table[i][j]
				print(f'{row[0].hex()} {row[1]}')
