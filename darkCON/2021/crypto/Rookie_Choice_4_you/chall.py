#!/usr/bin/env python3
from Crypto.Cipher import ARC4	# pip3 install pycryptodome
import os

KEY = os.urandom(16)
FLAG = "******************* REDUCTED *******************"

menu = """
+--------- MENU ---------+
|                        |
| [1] Show FLAG          |
| [2] Encrypt Something  |
| [3] Exit               |
|                        |
+------------------------+
"""

print(menu)

while 1:
	choice = input("\n[?] Enter your choice: ")

	if choice == '1':
		cipher = ARC4.new(KEY)
		enc = cipher.encrypt(FLAG.encode()).hex()
		print(f"\n[+] Encrypted FLAG: {enc}")

	elif choice == '2':
		plaintext = input("\n[*] Enter Plaintext: ")
		cipher = ARC4.new(KEY)
		ciphertext = cipher.encrypt(plaintext.encode()).hex()
		print(f"[+] Your Ciphertext: {ciphertext}")

	else:
		print("\n:( See ya later!")
		exit(0)
