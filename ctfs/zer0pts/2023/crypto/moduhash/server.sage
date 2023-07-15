import os

flag = os.environb.get(b"FLAG", b"dummmmy{test_test_test}")

def S(z):
	return -1/z

def T(z):
	return z + 1

def gen_random_hash(n):
	r = bytes([getrandbits(8) for _ in range(0, n)])
	return r

def to_hash(st):
	res = ""
	for s in st:
		sts = bin(s)[2:].zfill(8)
		for x in sts:
			if x == "0":
				res += "S"
			else:
				res += "T"
	return res

def hash(z, h):
	res = z
	for s in h:
		if s == "S":
			res = S(res)
		elif s == "T":
			res = T(res)
		else:
			exit()
	return res

def hash_eq(h1, h2, CC):
	for _ in range(100):
		zr = CC.random_element()
		h1zr = hash(zr, h1)
		h2zr = hash(zr, h2)
		if abs(h1zr - h2zr) > 1e-15:
			return False
	return True

CC = ComplexField(256)
for _ in range(100):
	n = randint(32, 64)
	h1 = to_hash(gen_random_hash(n))

	zi = CC.random_element()
	print(f"zi	: {zi}")
	print(f"h1(zi): {hash(zi, h1)}")

	h2 = input("your hash> ")

	if not hash_eq(h1, h2, CC):
		print("your hash is incorrect")
		exit()

print(flag)
