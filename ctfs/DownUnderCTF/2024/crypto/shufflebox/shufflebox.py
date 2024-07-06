import random

PERM = list(range(16))
random.shuffle(PERM)

def apply_perm(s):
	assert len(s) == 16
	return ''.join(s[PERM[p]] for p in range(16))

for line in open(0):
	line = line.strip()
	print(line, '->', apply_perm(line))
