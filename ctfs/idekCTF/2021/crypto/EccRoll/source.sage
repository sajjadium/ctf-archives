from Crypto.Util.number import bytes_to_long
import random
from secret import flag

def gen(nbits):

	p = random_prime(2^(nbits)+1, 2^(nbits))
	E = EllipticCurve(GF(p), [9487, 0])
	G = E.gens()[0]
	ord_G = G.order()

	### Remove small prime powers to avoid Pohlig-Hellman
	for i in range(2, 33):
		if ord_G % i == 0:
			G = i * G
			ord_G //= i

	### Make a relationship between generators, so it will
	### be much harder to guess the bits, right?
	g = (p - G.xy()[0])

	return p, G, g

def encrypt(bflag):

	p, G, g = gen(128)

	enc = []

	for b in bflag:
		### Haha, the outputs should be random enough 
		r = random.randint(2, p-1)
		if b == "0":
			enc += [(r * G).xy()[0]]
		else:
			enc += [pow(g, r, p)]

	return p, G, g, enc

bflag = bin(bytes_to_long(flag))[2:]

### I'm so kind, thus I'll give you 20 encryptions
for i in range(20):
	p, G, g, enc = encrypt(bflag)
	print("p = {}".format(p))
	print("G = {}".format(G))
	print("g = {}".format(g))
	print("enc = {}".format(enc))	

	

