#!/usr/bin/env python3

import random

MAX_DIGITS = 65536

def vault() -> bool:

	pin = "".join([random.choice("0123456789abcdef") for _ in range(4)])
	digits = ["z", "z", "z", "z"]
	counter = 0

	print("What is the 4-digit PIN?")

	while True:

		attempt = list(input("Attempt> "))

		for _ in range(len(attempt)):

			digits.insert(0, attempt.pop())
			digits.pop()

			if "".join(digits) == pin:
				return True

			counter += 1
			if counter > MAX_DIGITS:
				return False

	return False

def main():

	print("You're burgling a safehouse one night (as you often do) when you run into a")
	print("vault. The vault is protected by a 16-digit pad for a 4-digit PIN. The")
	print("safehouse is guarded by an alarm system and if you're not careful, it'll go")
	print("off, which is no good for you. After this, there are 15 more vaults.\n")

	for n in range(16):

		print(f"You've made it to vault #{n+1}.\n")

		print("|---|---|---|---|")
		print("| 0 | 1 | 2 | 3 |")
		print("|---|---|---|---|")
		print("|---|---|---|---|")
		print("| 4 | 5 | 6 | 7 |")
		print("|---|---|---|---|")
		print("|---|---|---|---|")
		print("| 8 | 9 | a | b |")
		print("|---|---|---|---|")
		print("|---|---|---|---|")
		print("| c | d | e | f |")
		print("|---|---|---|---|\n")

		if not vault():
			print("The alarm goes off and you're forced to flee. Maybe next time!")
			return
		print("You've defeated this vault.")

	print("You unlock the vault and find the flag.\n")
	with open("flag.txt", "r") as f:
		print(f.read(), end="")

if __name__ == "__main__":
	main()
