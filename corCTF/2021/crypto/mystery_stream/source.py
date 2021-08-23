from random import randrange
from secrets import flag, key
from Crypto.Util.number import long_to_bytes

def bsum(state, taps, l):
	ret = 0
	for i in taps:
		ret ^= (state >> (l - i))
	return ret & 1

class Gen:
	def __init__(self, key, slength):
		self.state = key
		self.slength = slength
		self.TAPS = [2, 4, 5, 7, 10, 12, 13, 17, 19, 24, 25, 27, 30, 32, 
		33, 34, 35, 45, 47, 49, 50, 52, 54, 56, 57, 58, 59, 60, 61, 64]

	def clock(self):
		out = bsum(self.state, self.TAPS, self.slength)
		self.state = (out << (self.slength - 1)) + (self.state >> 1)
		return out

def insertflag(fn, flag):
	txt = b''
	with open(fn, 'rb') as f:
		txt = f.read()
	i = randrange(0, len(txt))
	txt = txt[:i] + flag + txt[i:]
	with open(fn, 'wb') as f:
		f.write(txt)

def gf256_multiply(a,b):
  p = 0
  for _ in range(8):
    if b % 2:
      p ^= a
    check = a & 0x80
    a <<= 1
    if check == 0x80:
      a ^= 0x1b
    b >>= 1
  return p % 256

def encrypt(fn, outf, cipher):
	pt = b''
	with open(fn, 'rb') as f:
		pt = f.read()
	ct = b''
	for byte in pt:
		genbyte = 0
		for i in range(8):
			genbyte = genbyte << 1
			genbyte += cipher.clock()
		ct += long_to_bytes(gf256_multiply(genbyte, byte))
	with open(outf, 'wb') as f:
		f.write(ct)

insertflag('pt', flag)
cipher = Gen(key, 64)
encrypt('pt', 'ct', cipher)