#!/usr/local/bin/python

import os
from Crypto.Util.number import bytes_to_long

def LFSR():
	state = bytes_to_long(os.urandom(8))
	while 1:
		yield state & 0xf
		for i in range(4):
			bit = (state ^ (state >> 1) ^ (state >> 3) ^ (state >> 4)) & 1
			state = (state >> 1) | (bit << 63)

rng = LFSR()

n = 56

print(f"Let's play rock-paper-scissors! We'll give you {n} free games, but after that you'll have to beat me 50 times in a row to win. Good luck!")
rps = ["rock", "paper", "scissors", "rock"]

nums = []
for i in range(n):
	choice = next(rng) % 3
	inp = input("Choose rock, paper, or scissors: ")
	if inp not in rps:
		print("Invalid choice")
		exit(0)
	if inp == rps[choice]:
		print("Tie!")
	elif rps.index(inp, 1) - 1 == choice:
		print("You win!")
	else:
		print("You lose!")

for i in range(50):
	choice = next(rng) % 3
	inp = input("Choose rock, paper, or scissors: ")
	if inp not in rps:
		print("Invalid choice")
		break
	if rps.index(inp, 1) - 1 != choice:
		print("Better luck next time!")
		break
	else:
		print("You win!")
else:
	print(open("flag.txt").read())