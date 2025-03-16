from hashlib import sha256
from base64 import b64encode, b64decode

# utility wrapper for hashing

def digest(message):
	"Gives a bytes object representing the sha256 encoding of its argument (a sequence of bytes)"
	return sha256(message).digest()

# utility wrapper for encoding and decoding

def base64_encode(x):
	"Encodes a sequence of bytes in a string, using base64 encoding"
	return b64encode(x).decode()

def base64_decode(x):
	return b64decode(x, validate=True)

# crypto magic

def create_key(passphrase):
	h = passphrase.encode()
	h = digest(h)
	k = 0
	for i in range(8):
		k <<= 8
		k |= h[i]
	return k if k else 1

def secret_byte_stream(key):
	x = key
	mask = 255
	while True:
		y = x		# 64
		a = y & mask
		yield a
		y >>=  8
		x = y
		y >>=  1	# 45
		a ^= y & mask
		y >>= 14	# 31
		a ^= y & mask
		y >>= 17	# 14
		a ^= y & mask
		x |= a << 56

def scramble(message, key):
	stream = secret_byte_stream(key)
	return bytes(x ^ y for x, y in zip(message, stream))

# user-facing stuff

def encrypt(text, passphrase):
	message = text.encode()
	hash = digest(message)
	key = create_key(passphrase)
	e = scramble(message, key)
	return '#'.join(map(base64_encode, [e, hash]))

def decrypt(text, passphrase):
	e, hash = map(base64_decode, text.split('#'))
	key = create_key(passphrase)
	message = scramble(e, key)
	if hash != digest(message):
		raise ValueError("Wrong key")
	return message.decode()

def create_flag(secret):
	return "".join(["KSUS{", secret.encode().hex(), "}"])

if __name__ == "__main__":
	secret = input("secret > ")
	passphrase = input("passphrase > ")
	flag = create_flag(secret)
	print("flag :", flag)
	challenge = encrypt(flag, passphrase)
	assert flag == decrypt(challenge, passphrase)
	print("challenge :", challenge)
