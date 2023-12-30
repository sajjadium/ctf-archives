#!/usr/bin/env sage

from Crypto.Util.number import *
from secret import params, flag

class defcode:
	def __init__(self, n, m, g):
		t = g.degree()
		FM = g.base_ring()
		Z = FM.gen()
		RFM = g.parent()
		X = RFM.gen()
		CL = [Z^(_ + 1) for _ in range(2**m - 1)] + [FM(0)]
		h = RFM(1)
		for _ in CL: h *= (X - _)
		G = [(h * ((X - _).inverse_mod(g))).mod(g) for _ in CL]
		HCP = matrix(FM, t, n)
		for i in range(n):
			cfs = list(G[i])
			for j in range(t):
				if j < len(cfs): HCP[j,i] = cfs[j]
				else: HCP[j, i] = FM(0)
		H = matrix(F, m * HCP.nrows(), HCP.ncols())
		for i in range(HCP.nrows()):
			for j in range(HCP.ncols()):
				b = list(bin(eval(HCP[i, j]._int_repr()))[2:].zfill(m))
				H[m*i:m*(i+1), j] = vector(map(int, b))
		GG = H.right_kernel().basis_matrix()
		S = matrix(RFM, 1, len(CL))
		for _ in range(len(CL)):
			S[0, _] = (X - CL[_]).inverse_mod(g)
		self._n = n
		self._m = m
		self._g = g
		self._t = t
		self._CL = CL
		self._S = S
		self._H = H
		self._GG = GG

	def gx(self):
		return (self._GG)

class SONY_SYSTEM:
	def __init__(self, n, m, g):
		gc = defcode(n, m, g)
		k = gc.gx().nrows()
		S = matrix(GF(2), k, [random() < 0.5 for _ in range(k**2)])
		while rank(S) <= k - 1:
			S[floor(k * random()), floor(k * random())] += 1
		_r = list(range(n)) 
		P = matrix(GF(2), n)
		for i in range(n):
			p = floor(len(_r) * random())
			P[i, _r[p]] = 1
			_r = _r[:p] + _r[p+1:]

		self._m_defcode = gc
		self._g = g
		self._t = g.degree()
		self._S = S
		self._P = P
		self.pubkey = S * (self._m_defcode.gx()) * P

	def weight(self, n):
		w = 0
		for _ in range(n.ncols()):
			if n[0, _] == 1: w += 1
		return w

	def encrypt(self, msg):
		assert msg.ncols() == self.pub_key().nrows()
		ec = matrix(1, self.gc().gx().ncols())
		while self.weight(ec) < self.me():
			ec[0, randint(1, self.gc().gx().ncols() - 1)] = 1
		cd = msg * self.pub_key()
		return copy(cd + ec)

	def pub_key(self):
		return copy(self.pubkey)

	def gc(self):
		return copy(self._m_defcode)

	def me(self):
		return copy(self._t)

def ginv(f, g):
	u = xgcd(f, g)[1]
	return u.mod(g)

def ircp(t):
	while True:
		f = R.random_element(degree = t)
		if f.is_irreducible():
			g = R.random_element(degree = 13 + 37 * t)
			u = ginv(f, g)
			if u != 0:
				return f

def encode(msg, l):
	msg = bin(bytes_to_long(msg))[2:].zfill(l)
	assert len(msg) <= l
	M = matrix(GF(2), 1, l)
	for _ in range(l):
		M[0, _] = msg[_]
	return M

k, m, n, t = params

FM = GF(n, 'Z')
RFM = PolynomialRing(FM, 'X')

F = GF(2**m, 'g')
R = PolynomialRing(F, 'x')
f = ircp(t)

enc = SONY_SYSTEM(n, m, f)

flag = flag.lstrip(b'ASIS{').rstrip(b'}')
flag_1, flag_2 = flag[:16], flag[16:]

pubkey = [int(''.join([str(_) for _ in p]), 2) for p in enc.pub_key()]

M1 = encode(flag_1, enc.gc().gx().nrows())
M2 = encode(flag_2, enc.gc().gx().nrows())

enc_1 = enc.encrypt(M1)
enc_2 = enc.encrypt(M2)


print(f'f = {f}')
print(f'pubkey = {pubkey}')
print(f'enc_1 = {int("".join(str(enc_1)[1:-1].split()), 2)}')
print(f'enc_2 = {int("".join(str(enc_2)[1:-1].split()), 2)}')