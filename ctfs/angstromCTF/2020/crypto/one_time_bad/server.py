import random, time
import string
import base64
import os

def otp(a, b):
	r = ""
	for i, j in zip(a, b):
		r += chr(ord(i) ^ ord(j))
	return r


def genSample():
	p = ''.join([string.ascii_letters[random.randint(0, len(string.ascii_letters)-1)] for _ in range(random.randint(1, 30))])
	k = ''.join([string.ascii_letters[random.randint(0, len(string.ascii_letters)-1)] for _ in range(len(p))])

	x = otp(p, k)

	return x, p, k

random.seed(int(time.time()))

print("Welcome to my one time pad service!\nIt's so unbreakable that *if* you do manage to decrypt my text, I'll give you a flag!")
print("You will be given the ciphertext and key for samples, and the ciphertext for when you try to decrypt. All will be given in base 64, but when you enter your answer, give it in ASCII.")
print("Enter:")
print("\t1) Request sample")
print("\t2) Try your luck at decrypting something!")

while True:
	choice = int(input("> "))
	if choice == 1:
		x, p, k = genSample()
		print(base64.b64encode(x.encode()).decode(), "with key", base64.b64encode(k.encode()).decode())

	elif choice == 2:
		x, p, k = genSample()
		print(base64.b64encode(x.encode()).decode())
		a = input("Your answer: ").strip()
		if a == p:
			print(os.environ.get("FLAG"))
			break

		else:
			print("Wrong! The correct answer was", p, "with key", k)

