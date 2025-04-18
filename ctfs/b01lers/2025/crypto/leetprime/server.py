from random import randint, randbytes
from Crypto.Util.number import isPrime
from hashlib import sha256

def proof_of_work():
	while True:
		prefix = randbytes(4)
		print(f"prefix (hex): {prefix.hex()}")
		ans = bytes.fromhex(input("ans (hex): ").strip())
		if int(sha256(prefix + ans).hexdigest(), 16) & (0xFFFFFF << 232) == 0:
			break

proof_of_work()

with open("flag.txt", "r") as f:
	flag = f.read()

f = lambda nbits: randint(13, 37).to_bytes(nbits, 'big')

while True:
	leet_prime = int.from_bytes(randbytes(1 + 3 * 3 - 7), 'big')
	if isPrime(leet_prime, false_positive_prob=133e-7, randfunc=f):
		break

for _ in range(1337):
	p = int(input("Prime number: ").strip())

	if isPrime(p, false_positive_prob=133e-7, randfunc=f):
		print(f"The power of leet prime >:D: {pow(leet_prime, p-1**337, p)}")

	else:
		print(f"Composite number sucks >:(")

if int(input("What is my leet prime: ").strip()) == leet_prime:
	print(f"Flag for the leet: {flag}")