#!/usr/bin/env python3
import hashlib
from Crypto.Util.number import *

m = getRandomNBitInteger(128)

class User:
	def __init__(self, name, token):
		self.name = name
		self.mac = token

	def verifyToken(self):
		data = self.name.encode(errors="surrogateescape")
		crc = (1 << 128) - 1
		for b in data:
			crc ^= b
			for _ in range(8):
				crc = (crc >> 1) ^ (m & -(crc & 1))
		return hex(crc ^ ((1 << 128) - 1))[2:] == self.mac

def generateToken(name):
	data = name.encode(errors="surrogateescape")
	crc = (1 << 128) - 1
	for b in data:
		crc ^= b
		for _ in range(8):
			crc = (crc >> 1) ^ (m & -(crc & 1))
	return hex(crc ^ ((1 << 128) - 1))[2:]

def printMenu():
	print("1. Register")
	print("2. Login")
	print("3. Make a wish")
	print("4. Wishlist (Santa Only)")
	print("5. Exit")

def main():
	print("Want to make a wish for this Christmas? Submit here and we will tell Santa!!\n")
	user = None
	registered = False
	while(1):
		printMenu()
		try:
			option = int(input("Enter option: "))
			if option == 1:
				# User only can register once to fix forge token bug
				if registered:
					print("Ho Ho Ho! No cheating!")
					break
				name = str(input("Enter your name: "))
				if "Santa Claus" in name:
					print("Cannot register as Santa!\n")
					continue
				print(f"Use this token to login: {generateToken(name)}\n")
				registered = True
				
			elif option == 2:
				name = input("Enter your name: ")
				mac = input("Enter your token: ")
				user = User(name, mac)
				if user.verifyToken():
					print(f"Login successfully as {user.name}")
					print("Now you can make a wish!\n")
				else:
					print("Ho Ho Ho! No cheating!")
					break
			elif option == 3:
				if user:
					wish = input("Enter your wish: ")
					open("wishes.txt","a").write(f"{user.name}: {wish}\n")
					print("Your wish has recorded! Santa will look for it!\n")
				else:
					print("You have not login yet!\n")

			elif option == 4:
				if user and "Santa Claus" in user.name:
					wishes = open("wishes.txt","r").read()
					print("Wishes:")
					print(wishes)
				else:
					print("Only Santa is allow to access!\n")
			elif option == 5:
				print("Bye!!")
				break
			else:
				print("Invalid choice!")
		except Exception as e:
			print(str(e))
			break

if __name__ == "__main__":
	main()