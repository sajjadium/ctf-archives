#!/usr/local/bin/python

from hashlib import shake_128

# from Crypto.Util.number import getPrime
# p = getPrime(1024)
# q = getPrime(1024)
# n = p*q
n = 20074101780713298951367849314432888633773623313581383958340657712957528608477224442447399304097982275265964617977606201420081032385652568115725040380313222774171370125703969133604447919703501504195888334206768326954381888791131225892711285554500110819805341162853758749175453772245517325336595415720377917329666450107985559621304660076416581922028713790707525012913070125689846995284918584915707916379799155552809425539923382805068274756229445925422423454529793137902298882217687068140134176878260114155151600296131482555007946797335161587991634886136340126626884686247248183040026945030563390945544619566286476584591
T = 2**64

def is_valid(x):
	return type(x) == int and 0 < x < n

def encode(x):
	return x.to_bytes(256, 'big')

def H(g, h):
	return int.from_bytes(shake_128(encode(g) + encode(h)).digest(16), 'big')

def prove(g):
	h = g
	for _ in range(T):
		h = pow(h, 2, n)
	m = H(g, h)
	r = 1
	pi = 1
	for _ in range(T):
		b, r = divmod(2*r, m)
		pi = pow(pi, 2, n) * pow(g, b, n) % n
	return h, pi

def verify(g, h, pi):
	assert is_valid(g)
	assert is_valid(h)
	assert is_valid(pi)
	assert g != 1 and g != n - 1
	m = H(g, h)
	r = pow(2, T, m)
	assert h == pow(pi, m, n) * pow(g, r, n) % n

if __name__ == '__main__':
	g = int(input('g: '))
	h = int(input('h: '))
	pi = int(input('pi: '))
	verify(g, h, pi)
	with open('flag.txt') as f:
		print(f.read().strip())
