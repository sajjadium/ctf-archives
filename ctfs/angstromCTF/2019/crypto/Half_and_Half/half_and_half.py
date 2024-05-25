from secret import flag

def xor(x, y):
	o = ''
	for i in range(len(x)):
		o += chr(ord(x[i])^ord(y[i]))
	return o

assert len(flag) % 2 == 0

half = len(flag)//2
milk = flag[:half]
cream = flag[half:]

assert xor(milk, cream) == '\x15\x02\x07\x12\x1e\x100\x01\t\n\x01"'