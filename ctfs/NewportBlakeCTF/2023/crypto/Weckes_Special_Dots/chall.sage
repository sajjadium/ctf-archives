import random
from math import gcd
from Crypto.Util.number import bytes_to_long

ps = []
qs = []
Ns = []
for k in range(4):
	pk = random_prime(2^512)
	qk = random_prime(2^512)
	Nk = pk*qk

	Ns.append(Nk)
	qs.append(min([pk,qk]))
	ps.append(max([pk,qk]))

N = min(Ns)

sigma = 2/5
boundxy = int(N^sigma)

ys = [random.randint(0,boundxy^0.5) for _ in range(4)]
x = random.randint(0,boundxy^0.5)

zs = []
for i in range(4):
	while True:
		totient = (ps[i] - 1)*(qs[i] - 1)
		bound = (((ps[i] - qs[i])/(3*(ps[i] + qs[i])))*(N^0.25)*ys[i])
		z = x^2 - ((ys[i]^2*totient) % (x^2))
		if z < bound:
			zs.append(z)
			break

es = []
for i in range(4):
	totient = (ps[i] - 1)*(qs[i] - 1)
	e = int((zs[i] + ys[i]^2*totient) // (x^2))
	es.append(e)

for i in range(4):
	totient = (ps[i] - 1)*(qs[i] - 1)
	assert es[i]*x^2 - ys[i]^2*totient == zs[i]

flag = b"nbctf{[REDACTED]}"
flag = bytes_to_long(flag + b"\x00"*(96-len(flag)))

cts = []
for i in range(4):
	cts.append(pow(flag,es[i],Ns[i]))

print(f"{Ns = }")
print(f"{es = }")
print(f"{cts = }")
