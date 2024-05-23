#!/usr/bin/python3

from secrets import randbits
from sympy import nextprime
import random

e = random.randint(500,1000)

def encrypt(inp):
	p = nextprime(randbits(1024))
	q = nextprime(randbits(1024))
	n = p * q
	c = [pow(ord(m), e, n) for m in inp]
	return [n, c]

def main():
	
	while True:
		print('Welcome to the Really Shotty Asymmetric (RSA) Encryption Server!')
		print('1: Encrypt a message')
		print('2: View the encrypted flag')
		print('3: Exit')
		
		inp = ''
		while (not ('1' in inp or '2' in inp or '3' in inp)):
			inp = input('> ')
		
		if('3' in inp):
			print('Goodbye!')
			exit()

		elif('1' in inp):
			plain = input('Enter a message, and the server will encrypt it with a random N!\n> ')
			encrypted = encrypt(plain)

		elif('2' in inp):
			data = open('flag.txt', 'r').read()
			data = data.strip()
			encrypted = encrypt(data)

		print('Your randomly chosen N:')
		print(f'> {encrypted[0]}')
		print('Your encrypted message:')
		print(f'> {encrypted[1]}')
		print('\n')

if(__name__ == '__main__'):
	main()
