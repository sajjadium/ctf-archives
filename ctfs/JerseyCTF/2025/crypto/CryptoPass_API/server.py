#!/usr/local/bin/python
from Crypto.Cipher import AES
from random import seed,choices,randint
from os import urandom,environ
from string import ascii_letters,digits

seed(urandom(16))
charset = ascii_letters+digits

admin_id = "RokosBasiliskIsSuperCool"
master_key = urandom(16)

def crypt(data, iv, enc):
	if type(data) != bytes:
		data = data.encode("ascii")
	integrity = AES.new(key=master_key, mode=AES.MODE_CFB, iv=iv, segment_size=128)
	
	if enc:
		return iv,integrity.encrypt(data)
	else:
		return iv,integrity.decrypt(data)

def sign_user(name):
	iv, name_enc = crypt(name, urandom(16), True)
	token = ".".join([x.hex() for x in [iv, name_enc]])
	return token

def generate_admin(passwd: str):
	true_pwd = environ.get("DEV_PASSWD")
	if true_pwd == None:
		return "Admin authentication not enabled currently"

	if passwd == true_pwd:
		return sign_user(admin_id)
	else:
		return "Wrong password"

def generate_token():
	return sign_user("guest")

def info(token: str):
	try:
		token = token.split(".")
		iv = bytes.fromhex(token[0])
		data = crypt(bytes.fromhex(token[1]), iv, False)[1].decode("latin")

		#open the default greeting for guest users
		status = "ADMINISTRATOR" if data == admin_id else "USER"

		try:
			assert("." not in data)
			vault = open(f"vault/{data}","rb").read().hex()
		except (ValueError,FileNotFoundError,AssertionError):
			vault = "NO DATA"

		return vault
	except Exception as e:
		return "Invalid token"

while True:
	print("Hello! Welcome to the CryptoPass Terminal")
	print("[1] => Login as guest")
	print("[2] => Login as admin")
	print("[3] => Access your vault")

	try:
		inp = int(input("> ").strip())
	except ValueError:
		print()
		continue

	if inp == 1:
		print("Here is your access token, guest:")
		print(generate_token())
	elif inp == 2:
		pwd = input("Developer passcode: ").strip()
		print(generate_admin(pwd))
	elif inp == 3:
		token = input("Authorization Token: ").strip()
		print(info(token))

	print()
