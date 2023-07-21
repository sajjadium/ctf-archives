from random import getrandbits as grb
from Crypto.Util.number import getPrime as gp, isPrime as ip

FLAG = b"flag{REDACTED}"

class flavor:
	def __init__(self, state, mod):
		self.state = state
		self.mod = mod
		self.mult = grb(32)
		self.inc = grb(32)

	def gen(self):
		self.state = ((self.state * self.mult + self.inc) % self.mod)
		return self.state

def condiment(x):
	while not ip(x):
		x+=1
	return x

def cook(m, x):
	n = gp(64)
	res = ""
	for i in m:
		res += hex(pow(i, 4, n) ^ x.gen())[2:] + "xx"
	return res

def main():
	print('====================================')
	print('You are connected to : Αρχαία Γεύση ')
	print('   Please make yourself at home     ')
	print('====================================')
	while True:
		try:
			print('Food of the day:')
			print('1. Cook flagga')
			print('2. Cook your own menu')
			print('3. Exit')
			u = input('>> ')
			print('')
			if u == "1":#I wonder what will happen if i just use these values instead
				ingredients = flavor(condiment(grb(64)), condiment(grb(64)))
				print(f"Here's your food: {cook(FLAG, ingredients)}")
			elif u == "2":
				ingredients = flavor(gp(64), gp(64))
				print('Menu:')
				m = input(">> ").encode()
				print(f"Here's your food: {cook(m, ingredients)}")
			elif u == "3":
				print('See ya!')
				break
			print('')
		except:
			print('Error! Exiting...')
			break


if __name__ == "__main__":
	main()
