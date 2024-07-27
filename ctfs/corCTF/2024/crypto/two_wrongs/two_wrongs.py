from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
import numpy as np
import random, os, binascii, sys
from Crypto.Cipher import AES
from flag import flag

key = os.urandom(16)
cipher = AES.new(key, AES.MODE_ECB)

sv_sim = AerSimulator(method="statevector")
bit_idxs = list(map(int, input('Select a sensor index to remove from each bit: ').split(' ')))

def enc_byte(b):
	sensor_vals = ''
	bit_encs = []
	for bit in format(b, '08b'):
		seed = int.from_bytes(os.urandom(8), sys.byteorder)
		sensor_val = enc_bit(bit, seed)
		sensor_vals += ''.join(sensor_val.split(' '))
		bit_encs.append((bit, seed))
	sensor_vals = list(sensor_vals)
	for i in range(8):
		sensor_vals[i * 6 + bit_idxs[i]] = '?'
	return ''.join(sensor_vals), bit_encs

def rand_bit_flip(qc, main, seed):
	if seed % 3 == 0:
		qc.x(main[seed % 7])
	elif seed % 3 == 1:
		qc.z(main[seed % 7])

def enc_bit(bit, seed):
	main = QuantumRegister(7)
	anc_x = QuantumRegister(3)
	anc_z = QuantumRegister(3)
	syn_x = ClassicalRegister(3)
	syn_z = ClassicalRegister(3)

	qc = QuantumCircuit(main, anc_x, anc_z, syn_x, syn_z)

	if bit == '1':
		qc.initialize([0, 1], main[6])

	for i in range(3):
	    qc.h(main[i])

	qc.cx(main[6], main[3])
	qc.cx(main[6], main[4])

	for idx in [3,4,5]:
	    qc.cx(main[0], main[idx])

	for idx in [3,5,6]:
	    qc.cx(main[1], main[idx])

	for idx in [4,5,6]:
	    qc.cx(main[2], main[idx])

	rand_bit_flip(qc, main, seed)

	qc.h(anc_x)
	qc.h(anc_z)


	norms = [[1, 0, 0, 1, 1, 1, 0],
	         [0, 1, 0, 1, 0, 1, 1],
	         [0, 0, 1, 0, 1, 1, 1]]

	for i in range(3):
	    for j in range(len(norms[i])):
	        if norms[i][j] == 1:
	            qc.cx(anc_x[i], main[j])
	            qc.cz(anc_z[i], main[j])

	qc.h(anc_x)
	qc.h(anc_z)
	qc.measure(anc_x, syn_x)
	qc.measure(anc_z, syn_z)

	cc = transpile(qc, sv_sim)
	result = sv_sim.run(cc).result()
	sv = [*result.get_counts()][0]
	return sv

def run_insts(qc, main, res, insts):
	for inst in insts:
		toks = inst.split(' ')
		if len(toks) < 2 or len(toks) > 3:
			continue
		arg1 = res if toks[1] == 'r' else main[int(toks[1])]
		if len(toks) == 3:
			arg2 = res if toks[2] == 'r' else main[int(toks[2])]
		if toks[0] == 'x':
			qc.x(arg1)
		elif toks[0] == 'y':
			qc.y(arg1)
		elif toks[0] == 'z':
			qc.z(arg1)
		elif toks[0] == 'h':
			qc.h(arg1)
		elif toks[0] == 'cx':
			qc.cx(arg1, arg2)
		elif toks[0] == 'cy':
			qc.cy(arg1, arg2)
		elif toks[0] == 'cz':
			qc.cz(arg1, arg2)
		else:
			exit()

def measure_bit(bit, seed, insts):
	main = QuantumRegister(7)
	res = QuantumRegister(1)
	ans = ClassicalRegister(1)
	anc_x = QuantumRegister(3)
	anc_z = QuantumRegister(3)
	syn_x = ClassicalRegister(3)
	syn_z = ClassicalRegister(3)

	qc = QuantumCircuit(main, res, ans, anc_x, anc_z, syn_x, syn_z)

	if bit == '1':
		qc.initialize([0, 1], main[6])

	for i in range(3):
	    qc.h(main[i])

	qc.cx(main[6], main[3])
	qc.cx(main[6], main[4])

	for idx in [3,4,5]:
	    qc.cx(main[0], main[idx])

	for idx in [3,5,6]:
	    qc.cx(main[1], main[idx])

	for idx in [4,5,6]:
	    qc.cx(main[2], main[idx])

	rand_bit_flip(qc, main, seed)

	qc.h(anc_x)
	qc.h(anc_z)

	norms = [[1, 0, 0, 1, 1, 1, 0],
	         [0, 1, 0, 1, 0, 1, 1],
	         [0, 0, 1, 0, 1, 1, 1]]

	for i in range(3):
	    for j in range(len(norms[i])):
	        if norms[i][j] == 1:
	            qc.cx(anc_x[i], main[j])
	            qc.cz(anc_z[i], main[j])

	qc.h(anc_x)
	qc.h(anc_z)
	qc.measure(anc_x, syn_x)
	qc.measure(anc_z, syn_z)

	run_insts(qc, main, res, insts)

	qc.measure(res, ans)

	cc = transpile(qc, sv_sim)
	result = sv_sim.run(cc).result()
	sv = [*result.get_counts()][0]
	return sv[-1]

print("Here's your flag:", binascii.hexlify(cipher.encrypt(flag.encode())))
print("Alright, good luck decoding.")
for b in key:
	sens, bits = enc_byte(b)
	print('Sensor measurements:', sens)
	insts = []
	print('Help me decode, one bit per line, instructions (ex. x 1, z 2) separated by semicolons:')
	print('You can only touch main or res. Use an integer to index main, or r for res.')
	for _ in range(len(bits)):
		inst_set = input('').split(';')
		insts.append(inst_set)
	bit_ans = ''
	print(insts)
	for i in range(len(bits)):
		bit, seed = bits[i]
		bit_ans += measure_bit(bit, seed, insts[i])
	print('Your byte:', bit_ans)
	print('On to the next byte!')