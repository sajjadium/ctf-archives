import numpy
from flag import flag

def convert_to_bits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def non_singular_matrix():
	x = random_matrix(ZZ, 32)
	if (x.det() == 0):
		non_singular_matrix()
	return x

def encrypt(flag):
	bits = convert_to_bits(flag)
	enc = []
	z = random_matrix(ZZ, 32, algorithm='unimodular')

	for bit in bits:
		x = non_singular_matrix()
		y = non_singular_matrix()
		if bit:
			y = x*z
		enc.append((x,y))

	return enc

encrypted = encrypt(flag)
numpy.save('enc.npy', encrypted)