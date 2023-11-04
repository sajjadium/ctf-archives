def str2bits(s):
	table = "}{_0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxy"
	s = "".join("{0:06b}".format(table.index(c)) for c in s)
	return s

FLAG="TSGCTF{Dummy}"

with open('problem_base','r') as fp:
	rle = fp.read()

for b in str2bits(FLAG):
	if b == "0":
		rle = rle.replace("@",".",1)
		rle = rle.replace("@","A",1)
	else:
		rle = rle.replace("@","C",1)
		rle = rle.replace("@",".",1)

rle = rle.replace("@",".")

with open('problem.rle','w') as fp:
	fp.write(rle)

