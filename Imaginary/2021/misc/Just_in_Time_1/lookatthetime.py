#!/usr/bin/env python3

import time
import random

def main():
	time.sleep(random.random())
	random.seed(round(time.time(), 2))
	print("If you guess my numbers, I'll give you the flag.")
	print("I'll give you a hint: %d"%random.randint(0, 1000000000))
	for i in range(3):
		try:
			rnum = random.randint(0, 1000000000)
			num = int(input("What is number %d? "%(i+1)))
			if num != rnum:
				raise Exception()
		except Exception as e:
			print("Nope! Try again later...")
			return
	print("Well done!")
	print(open('flag.txt', 'r').read())

if __name__ == '__main__':
	main()