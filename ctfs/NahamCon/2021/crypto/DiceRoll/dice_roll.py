#!/usr/bin/env python3

import random
import os

banner = """
              _______
   ______    | .   . |\\
  /     /\\   |   .   |.\\
 /  '  /  \\  | .   . |.'|
/_____/. . \\ |_______|.'|
\\ . . \\    /  \\ ' .   \\'|
 \\ . . \\  /    \\____'__\\|
  \\_____\\/

      D I C E   R O L L
"""

menu = """
0. Info
1. Shake the dice
2. Roll the dice (practice)
3. Guess the dice (test)
"""

dice_bits = 32
flag = open('flag.txt').read()

print(banner)

while 1:
	print(menu)

	try:
		entered = int(input('> '))
	except ValueError:
		print("ERROR: Please select a menu option")
		continue

	if entered not in [0, 1, 2, 3]:
		print("ERROR: Please select a menu option")
		continue

	if entered == 0:
		print("Our dice are loaded with a whopping 32 bits of randomness!")
		continue

	if entered == 1:
		print("Shaking all the dice...")
		random.seed(os.urandom(dice_bits))
		continue

	if entered == 2:
		print("Rolling the dice... the sum was:")
		print(random.getrandbits(dice_bits))
		continue

	if entered == 3:
		print("Guess the dice roll to win a flag! What will the sum total be?")
		try:
			guess = int(input('> '))
		except ValueError:
			print("ERROR: Please enter a valid number!")
			continue

		total = random.getrandbits(dice_bits)
		if guess == total:
			print("HOLY COW! YOU GUESSED IT RIGHT! Congratulations! Here is your flag:")
			print(flag)
		else:
			print("No, sorry, that was not correct... the sum total was:")
			print(total)

		continue

