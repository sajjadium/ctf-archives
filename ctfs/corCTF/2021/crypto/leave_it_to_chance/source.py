from Crypto.Util.number import getPrime
from random import randrange, shuffle
from private import flag

class Game():
	KEY_LEN = 32

	def __init__(self):
		self.p = getPrime(256)
		while self.p % 4 == 3:
			self.p = getPrime(256)
		x = randrange(self.p)
		while pow(x, (self.p-1)//2, self.p) == 1:
			x = randrange(self.p)
		self.a = pow(x, (self.p-1)//4, self.p)
		self.privgen()
		self.signed = []

	def privgen(self):
		self.priv = [randrange(self.p) for _ in range(self.KEY_LEN)]

	def sign(self, m):
		s = 0
		for i in range(len(self.priv)):
			s += (pow(m, i, self.p) * self.priv[i]) % self.p
		return s

	def verify(self, m, s):
		c = self.sign(m)
		return c**4 % self.p == s

def getSig():
	m = int(input("Enter the message you would like to sign, in hex> "), 16) % game.p
	if m not in game.signed:
		s = game.sign(m)
		game.signed.append(m)
		print(f"Signature: {hex(s**4 % game.p)[2:]}")
		hints = [-s % game.p, s*game.a % game.p, -s*game.a % game.p]
		shuffle(hints)
		guess = int(input("Enter a guess for s, in hex> "), 16)
		if guess in hints:
			hints.remove(guess)
		print(f"Hints: {hints[0]} {hints[1]}")
	else:
		print("You already signed that.")

def verifyPair():
	m = int(input("Enter m, in hex> "), 16)
	s = int(input("Enter s, in hex> "), 16)
	if game.verify(m, s):
		print("Valid signature.")
	else:
		print("Invalid signature.")

def guessPriv():
	inp = input("Enter the private key as a list of space-separated numbers> ")
	guess = [int(n) for n in inp.split(" ")]
	if guess == game.priv:
		print(f"Nice. Here's the flag: {flag}")
	else:
		print("No, that's wrong.")
	exit()

def menu():
	print("Enter your choice:")
	print("[1] Get a signature")
	print("[2] Verify a message")
	print("[3] Guess the private key")
	print("[4] Exit")
	options = [getSig, verifyPair, guessPriv, exit]
	choice = int(input("Choice> "))
	if choice - 1 in range(len(options)):
		options[choice - 1]()
	else:
		print("Please enter a valid choice.")

game = Game()
welcome = f"""Welcome.
I will let you sign as many messages as you want.
If you can guess the private key, the flag is yours.
But you only have one chance. Make it count.
p = {game.p}
"""
print(welcome)
while True:
	menu()