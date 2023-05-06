from Crypto.Util.number import getPrime
from hashlib import sha256
import random


def gen_parameters():
	p = getPrime(512)
	q = getPrime(512)
	N = p * q
	a = -3
	while True:
		b = random.randint(0, N)
		if (4*a**3 + 27*b**2) % N != 0:
			break
	x = random.randint(0, N)
	while True:
		y2 = (x**3 + a*x + b) % N
		if Zmod(p)(y2).is_square() and Zmod(q)(y2).is_square():
			break
		x = random.randint(0, N)
	y = CRT([int(Zmod(p)(y2).sqrt()), int(Zmod(q)(y2).sqrt())], [p, q])
	return (N, a, b, (x, y))

with open("flag.txt", "rb") as f:
	FLAG = f.read().strip()


N, a, b, (x, y) = gen_parameters()

EC = EllipticCurve(Zmod(N), (a, b))
P = EC(x, y)

T = P
ct = []
for byte in FLAG:
	r = int(T.xy()[0])
	ct.append(pow(byte*r, 65537, N))
	T += T

with open("backdoor.txt", "w") as f:
	f.write(str(P.xy()))

print(N)
print(a)
print(b)
print(ct)