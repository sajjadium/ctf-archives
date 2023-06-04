#!/usr/bin/env python3
import readline
import os
import random
import json
from Crypto.Cipher import AES

FLAG = os.getenv("FLAG")
assert FLAG is not None
key_hex = os.getenv("KEY")
assert key_hex is not None
KEY = bytes.fromhex(key_hex)

money = 0.0
r = random.SystemRandom()

def flag():
	if money < 1000000000:
		print("Not enough money\n")
	else:
		print(FLAG + "\n")

def play():
	global money
	cont = True
	while cont:
		print("Enter bet")
		try:
			bet = int(input("> "))
		except ValueError:
			print("Invalid bet")
		else:
			if bet > 5 or bet < 0:
				print("Invalid bet")
			else:
				winnings = round(bet * r.uniform(-2, 2), 2)
				money += winnings
				print(f"You won {winnings:.2f} coins! You now have {money:.2f} coins\n")
				while True:
					print("""Choose an option:
1. Continue
2. Return to menu""")
					try:
						inp = int(input("> "))
					except ValueError:
						print("Invalid choice")
					else:
						if inp == 1:
							break
						elif inp == 2:
							cont = False
							break
						else:
							print("Invalid choice")

def load():
	global money
	print("Enter token:")
	try:
		nonce, ciphertext = map(bytes.fromhex, input("> ").split("."))
	except ValueError:
		print("Invalid token")
	else:
		cipher = AES.new(KEY, AES.MODE_CTR, nonce=nonce)
		plaintext = cipher.decrypt(ciphertext)
		print(plaintext)
		money = json.loads(plaintext)["money"]

def save():
	cipher = AES.new(KEY, AES.MODE_CTR)
	plaintext = json.dumps({"money": money}).encode("utf-8")
	ciphertext = cipher.encrypt(plaintext)
	print(f"Save token: {cipher.nonce.hex()}.{ciphertext.hex()}")

def main():
	try:
		while True:
			print(
				f"""You have {money:.2f} coins.
Choose an option:
1. Get flag
2. Play
3. Enter save token
4. Quit"""
			)
			try:
				inp = int(input("> "))
			except ValueError:
				print("Invalid choice")
			else:
				if inp == 1:
					flag()
				elif inp == 2:
					play()
				elif inp == 3:
					load()
				elif inp == 4:
					save()
					return
				else:
					print("Invalid choice")
	except (EOFError, KeyboardInterrupt):
		pass

if __name__ == "__main__":
	main()