#!/usr/bin/env -S python3 -u

from Crypto.Util.number import *
from hidden import p, q, flag1

e = 65537
n = p*q
ns = str(n)
ctxt = pow(bytes_to_long(flag1), e, n)

class SneakyUserException(Exception):
	pass

def print_ctxt(t):
	print("Here's the encrypted message:", t)
	print("e =", e)
	print("n =", ns)

def encrypt():
	global e, n, ctxt
	ptxt = bytes_to_long(input("What's your message to encrypt? ").encode("utf8"))
	print_ctxt(pow(ptxt, e, n))

def decrypt():
	global e, p, q, n, ctxt
	try:
		c = int(input("What's your message to decrypt? "))
		if c == ctxt:
			raise SneakyUserException
		d = pow(e, -1, (p-1)*(q-1))
		m = pow(c, d, n)
		pt = long_to_bytes(m)
		if pt == flag1:
			raise SneakyUserException
		print("The decrypted message is",m)
		print()
		try:
			print("That spells out \""+pt.decode("utf8")+"\" if that means anything to you.")
		except UnicodeDecodeError as u:
			print("I couldn't figure out what that says ... are you sure you're doing it correctly?")
	except SneakyUserException as e:
		print("Hey, that's cheating! You can't ask me to decrypt the flag!")
		print("I'm not playing with you any more! Go cheat somewhere else.")
		exit()

def menu():
	print()
	print()
	print("1: Get Encrypted Flag")
	print("2: Encrypt Message")
	print("3: Decrypt Message")
	print("4: Quit")
	print()
	choice = int(input(">>> "))
	if choice == 1:
		print_ctxt(ctxt)
		print()
		print("Good luck!")
	elif choice == 2:
		encrypt()
	elif choice == 3:
		decrypt()
	elif choice == 4:
		print("Come back again soon!")
		exit()

if __name__ == '__main__':
	print("Hi! I'm Timmy! Have you come to play with my encryption system?")
	print("Just let me know what I can do for you!")
	while True:
		try:
			menu()
		except Exception as ex:
			print("Something's gone horribly wrong.")
			print("I have to go now. Bye!")
			exit()