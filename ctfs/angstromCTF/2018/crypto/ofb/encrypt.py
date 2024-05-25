import struct

def lcg(m, a, c, x):
	return (a*x + c) % m

m = pow(2, 32)

with open('lcg') as f:
	a = int(f.readline())
	c = int(f.readline())
	x = int(f.readline())

d = open('flag.png').read()
d += '\x00' * (-len(d) % 4)
d = [d[i:i+4] for i in range(0, len(d), 4)]

e = ''
for i in range(len(d)):
	e += struct.pack('>I', x ^ struct.unpack('>I', d[i])[0])
	x = lcg(m, a, c, x)

with open('flag.png.enc', 'w') as f:
	f.write(e)
	f.close()