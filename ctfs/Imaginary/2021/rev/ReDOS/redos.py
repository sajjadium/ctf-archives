#!/usr/local/bin/python

import re
# https://pypi.org/project/timeout-decorator/
import timeout_decorator

currentUser = None
users = {"admin@gmail.com":"REDACTED"}
emailRegex = re.compile(r'[A-Za-z0-9]+@((gmail)+)*\.(com|org|edu|gg)')

class TimeoutError(Exception):
	pass

def checkUserExists(email):
	return email in users.keys()

def login():
	global currentUser
	email = input("Email: ")
	if not checkUserExists(email):
		print("Sorry, we couldn't find that user in our database.")
		return
	pw = input("Password: ")
	if pw == users[email]:
		currentUser = email
		print("Login success!")
	else:
		print("Credentials incorrect.")

def getNewPass(email):
	pw = input("Password (at least 8 chars): ")
	pw2 = input("Enter Password Again: ")
	if len(pw) < 8:
		print("Sorry, that password doesn't match our security standards.")
		return None
	if pw != pw2:
		print("Those passwords don't match!")
		return None
	users[email] = pw
	return pw

@timeout_decorator.timeout(10, timeout_exception=TimeoutError)
def validateEmail(email):
	return emailRegex.match(email) is not None

def createAcc():
	email = input("Email: ")
	if not validateEmail(email):
		print("Sorry, that's not a valid email.")
		return
	if checkUserExists(email):
		print("Sorry, that user already exists in our database.")
		return
	if getNewPass(email) is not None:
		print("Account creation successful! Please login as your new account.")

def changePass():
	if currentUser == None:
		print("You are not currently logged in!")
		return
	currpw = input("Please enter your current password: ")
	if currpw != users[currentUser]:
		print("Credentials incorrect.")
		return
	if getNewPass(currentUser) is not None:
		print("Password changed successfully!")

def menu():
	print()
	print("="*80)
	print()
	if currentUser is not None:
		print("Hello {}!".format(currentUser))
		print("Welcome back to Super Secure Server(tm)!")
		print("1. Change User")
	else:
		print("Welcome to Super Secure Server(tm)!")
		print("1: Login")
	print("2: Create Account")
	print("3: Change Password")
	print()
	inp = input("Enter your choice: ")
	print()
	if '1' in inp:
		login()
	if '2' in inp:
		createAcc()
	if '3' in inp:
		changePass()

if __name__ == '__main__':
	try:
		while True:
			menu()
	except TimeoutError as e:
		print("Catastrophic Error")
		print("Error code: "+open("flag.txt", "r").read())
		print()
		print("Server shutting down...")
