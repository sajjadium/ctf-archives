from Crypto.Util.number import *
import blocks_sage as blocks # this is generated from blocks.sage
import random

seed = random.randint(2,2^255)

chain = blocks.Chain(seed)
priv_key = chain.ecdsa.priv_key
flag = chain.flag

welcome = """
WELCOME TO THE BLOCKCHAIN GENERATION!!!
WHERE ALL YOUR BLOCKCHAIN DREAMS COME TRUE!
SIGN AWAY!
"""
print(welcome)

idx = 1
while True:
	menu = "[1] Commit a message\n[2] View blocks\n[3] Verify Signature\n[4] Get Flag"
	print(menu)
	choice = int(input(": "))
	if choice == 1:
		message = bytes.fromhex(input("Enter (hex) string here: "))
		chain.commit(message, idx)
		print("Done")
		idx += 1
	elif choice == 2:
		dictionary = chain.view_messages()
		for i in range(len(dictionary)):
			print(f"Block {i}")
			print(f"Message {dictionary[i][0].hex()}")
			print(f"Signature {dictionary[i][1]}")
	elif choice == 3:
		r = int(input("r: "))
		s = int(input("s: "))
		message = bytes.fromhex(input("msg: "))
		opp = chain.verify_sig(r, s, message)
		if opp == True:
			print("It's valid!!")
		else:
			print("Darn, try again next time...")
	elif choice == 4:
		print("So you think you can get the flag huh? Try your luck.")
		if int(input("Private Key: ")) == priv_key:
			print(f"You must be our admin. Here's the flag {flag}")
			exit()
		else:
			print("NOOOOOOO")
			exit()
	else:
		print("What is that? Are you trying to hack me?")
		exit()