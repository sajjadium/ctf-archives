#!/usr/bin/env python3

from Crypto.Util.number import *
import sys
from flag import flag

flag = bytes_to_long(flag)
assert 256 < flag.bit_length() < 512

def die(*args):
	pr(*args)
	quit()

def pr(*args):
	s = " ".join(map(str, args))
	sys.stdout.write(s + "\n")
	sys.stdout.flush()

def sc(): return sys.stdin.readline().strip()

def main():
	border = "|"
	pr(border*72)
	pr(border, "Hi crypto-experts, send us your prime and we will mix the flag with ", border)
	pr(border, "it! Now can you find the flag in the mixed watery soup!? Good luck! ", border)
	pr(border*72)
	while True:
		pr("| Options: \n|\t[S]end the prime! \n|\t[Q]uit")
		ans = sc().lower()
		if ans == 's':
			pr(border, "Send your prime here: ")
			p = sc()
			try: p = int(p)
			except: die(border, "Your input is not valid!!")
			if not (128 <= p.bit_length() <= 224): die(border, "Your prime is out of bounds :(")
			if not isPrime(p): die(border, "Your input is NOT prime! Kidding me!?")
			pr(border, "Send the base here: ")
			g = sc()
			try: g = int(g) % p
			except: die("| Your base is not valid!!")
			if not (64 < g.bit_length() < 128): die(border, "Your base is too small!!")
			result = (pow(g ** 3 * flag, flag - g, p) * flag + flag * flag + g) % p
			pr(border, f"WooW, here is the mixed flag: {result}")
		elif ans == 'q': die(border, "Quitting ...")
		else: die(border, "Bye ...")

if __name__ == '__main__': main()