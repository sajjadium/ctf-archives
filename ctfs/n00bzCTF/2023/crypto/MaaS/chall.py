#!/usr/bin/python3
import random
from Crypto.Util.number import *
flag = open('flag.txt').read()
alpha = 'abcdefghijklmnopqrstuvwxyz'.upper()
to_guess = ''
for i in range(16):
	to_guess += random.choice(alpha)
for i in range(len(to_guess)):
	for j in range(3):
		inp = int(input(f'Guessing letter {i}, Enter Guess: '))
		guess = inp << 16
		print(guess % ord(to_guess[i]))
last_guess = input('Enter Guess: ')
if last_guess == to_guess:
	print(flag)
else:
	print('Incorrect! Bye!')
	exit()