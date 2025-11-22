import math, sys

inp = input("Enter your flag... ").encode()

s = int.from_bytes(inp)

o = (
	(6, 0, 7),
	(8, 2, 1),
	(5, 4, 3)
)

c = math.floor(math.log(s, 3))

if not c % 2:
	sys.stderr.write("Error: flag length needs to be even (hint: but in what base system?)!\n")
	sys.exit(1)

ss = 0

while c > -1:
	ss *= 9
	ss += o[s//3**c][s%3]
	
	s -= s//3**c*3**c
	s //= 3
	c -= 2

open("encrypted", 'wb').write(ss.to_bytes(math.ceil(math.log(ss, 256)), byteorder='big'))