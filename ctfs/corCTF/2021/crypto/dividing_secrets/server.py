from Crypto.Util.number import bytes_to_long, getStrongPrime
from random import randrange
from secret import flag

LIMIT = 64

def gen():
	p = getStrongPrime(512)
	g = randrange(1, p)
	return g, p

def main():
	g, p = gen()
	print("g:", str(g))
	print("p:", str(p))
	x = bytes_to_long(flag)
	enc = pow(g, x, p)
	print("encrypted flag:", str(enc))
	ctr = 0
	while ctr < LIMIT:
		try:
			div = int(input("give me a number> "))
			print(pow(g, x // div, p))
			ctr += 1
		except:
			print("whoops..")
			return
	print("no more tries left... bye")

main()	

