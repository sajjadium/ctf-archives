import os, sys
class TAES_Oracle:
	rounds = 10
	keysize = 10

	s_box = (
	0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
	0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
	0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
	0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
	0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
	0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
	0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
	0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
	0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
	0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
	0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
	0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
	0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
	0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
	0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
	0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
	)
	Constants = [
		0x11465e437e87fc55bc1f450ee0193d2a,
		0xb545ae3dddfb8f91c84b346ab8226046,
		0x458cabf5a74d0270d54b939e24926cfc,
		0x49a02a9bf60fb2f74ca3b1b1904d14c7,
		0x7dfa3b1ee676f340424d6fd9eebd0909,
		0xf95f40888714e16c3bdd03dfbf2ce276,
		0xa667b0c65ffb7cd36854e78fe9cfd066,
		0xae3874359710d933b553eb36251fec3d,
		0xd7f1fb018252bbed382d36449c702af5,
		0xf9d1a0eba064ba69c8b46c356ff02d79
	]


	def __init__(self):
		self.key = bytearray(os.urandom(self.keysize))

	def _sub_bytes(self, s):
		for i in range(4):
			for j in range(4):
				s[i][j] = self.s_box[s[i][j]]


	def _shift_rows(self, s):
		s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
		s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
		s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]


	def _add_round_key(self, s, k):
		for i in range(4):
			for j in range(4):
				s[i][j] ^= k[i][j]


	_xtime = lambda self, a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)


	def _mix_single_column(self, a):
		# see Sec 4.1.2 in The Design of Rijndael
		t = a[0] ^ a[1] ^ a[2] ^ a[3]
		u = a[0]
		a[0] ^= t ^ self._xtime(a[0] ^ a[1])
		a[1] ^= t ^ self._xtime(a[1] ^ a[2])
		a[2] ^= t ^ self._xtime(a[2] ^ a[3])
		a[3] ^= t ^ self._xtime(a[3] ^ u)


	def _mix_columns(self, s):
		for i in range(4):
			self._mix_single_column(s[i])


	def _bytes2matrix(self, text):
		""" Converts a 16-byte array into a 4x4 matrix.  """
		return [list(text[i:i+4]) for i in range(0, len(text), 4)]


	def _matrix2bytes(self, matrix):
		""" Converts a 4x4 matrix into a 16-byte array.  """
		return bytes(sum(matrix, []))


	def _expand_key(self, key):
		perm = [4, 3, 6, 2, 5, 8, 7, 0, 9, 1]
		key_bytes = list(key)
		assert(len(key_bytes) == 10)
		round_keys = []

		for i in range(self.rounds):
			rk = []
			rk.append( [key_bytes[i] for i in range(4)] )
			rk.append( [key_bytes[i] for i in range(4, 8)] )
			rk.append( [key_bytes[i] for i in range(4)] )
			rk.append( [key_bytes[i] for i in range(4, 8)] )

			round_keys.append(rk)

			p_key_bytes = [0] * 10

			for p in range(10):
				p_key_bytes[perm[p]] = key_bytes[p]

			key_bytes = p_key_bytes
			key_bytes[0] = self.s_box[key_bytes[0]]


		rk = []
		rk.append( [0]*4 )
		rk.append( [0]*4 )
		rk.append( [key_bytes[i] for i in range(4)] )
		rk.append( [key_bytes[i] for i in range(4, 8)] )
		round_keys.append(rk)
		
		return round_keys


	def _expand_tweak(self, tweak_bits):
		assert(len(tweak_bits) == 128)
		round_tweaks = []

		for i in range(self.rounds):
			rt = [bytes(4), bytes(4)]
			tweak2 = []
			tweak3 = []

			for j in range(4):
				tweak2_byte = ""
				tweak3_byte = ""
				for b in range(8):
					tweak2_byte += tweak_bits[ (11*(i+1) + (j*8) + b) % 128 ]
					tweak3_byte += tweak_bits[ (11*(i+1) + 32 + (j*8) + b) % 128 ]

				tweak2.append( int(tweak2_byte, 2) )
				tweak3.append( int(tweak3_byte, 2) )

			rt.append(bytes(tweak2))
			rt.append(bytes(tweak3))

			round_tweaks.append(rt)

		return round_tweaks


	def _add_constants(self, p, r):

		for col in range(4):
			for row in range(4):
				con = (self.Constants[r] >> (((3-col)*4 + (3-row)) * 8)) & ((1<<8) - 1)

				p[col][row] ^= con


	def encrypt(self, plaintext, tweak):
		p = self._bytes2matrix(plaintext)
		tweak = bin(int(tweak, 16))[2:].zfill(128)
		round_keys = self._expand_key(self.key)
		round_tweaks = self._expand_tweak(tweak)

		for i in range(self.rounds - 1):
			self._add_round_key(p, round_keys[i])
			self._add_round_key(p, round_tweaks[i])
			self._add_constants(p, i)

			self._sub_bytes(p)
			self._shift_rows(p)
			self._mix_columns(p)

		self._add_round_key(p, round_keys[self.rounds-1])
		self._add_round_key(p, round_tweaks[self.rounds-1])
		self._add_constants(p, self.rounds-1)
		self._sub_bytes(p)
		self._shift_rows(p)
		self._add_round_key(p, round_keys[self.rounds])

		return self._matrix2bytes(p)

