from decimal import Decimal, getcontext

from Crypto.Util.number import bytes_to_long, getRandomNBitInteger


def is_valid_privkey(n):
	if n < 0:
		return False
	c = n * 4 // 3
	d = c.bit_length()
	a = d >> 1
	if d & 1:
		x = 1 << a
		y = (x + (n >> a)) >> 1
	else:
		x = (3 << a) >> 2
		y = (x + (c >> a)) >> 1
	if x != y:
		x, y = y, (y + n // y) >> 1
		while y < x:
			x, y = y, (y + n // y) >> 1
	x = round(x)
	return all(i**2 != n for i in range(x - 1000, x + 1000))

def gen_secret_key():
	while True:
		sec = getRandomNBitInteger(128)
		if is_valid_privkey(sec):
			return sec

class PRNG:
	def __init__(self, key):
		getcontext().prec = 1000
		self.secret_key = key
		self.state = [int(i) for i in str(Decimal(self.secret_key).sqrt()).split(".")[-1]]

	def encrypt(self, message):
		m = [int(i) for i in str(bytes_to_long(message))]
		s = self.state[:len(m)]
		self.state = self.state[len(m):]
		return "".join(hex(i^j)[-1] for i,j in zip(m, s))

if __name__ == "__main__":
	secret_key = gen_secret_key()
	rng = PRNG(key=secret_key)
	print(rng.encrypt(b'My cryptographic message.'))
	print(rng.encrypt(b"THIS_FLAG_IS_REDACTED_LMAO"))
