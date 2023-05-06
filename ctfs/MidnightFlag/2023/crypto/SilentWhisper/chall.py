#!/usr/bin/env python3


from Crypto.Cipher import AES

import random

def cipherData(data,key):
	cipher = AES.new(key, AES.MODE_ECB)
	data = cipher.encrypt(data)
	return data

def decipherData(data,key):
	cipher = AES.new(key, AES.MODE_ECB)
	data = cipher.decrypt(data)
	return data


def pad(data):
	toPadd = 16 - (len(data) % 16)
	res = data + (toPadd).to_bytes(1,'big') * toPadd
	return res

def unpad(data):
	toUnpad = data[-1]
	return data[:-toUnpad]



key = bytearray(random.getrandbits(8) for _ in range(16))


for _ in range(10):

	choice = input("Choice : ")

	if not choice in ['1','2','3']:
		continue


	if choice == '1':

		username = input("enter your username : ")

		if len(username) > 32:
			username = username[:32]

		payload = "host:127.0.01,flag:MCTF{REDACTED},garbage:AAAAAAAAAAAAAAAAAAAA,username:" + username

		data = payload.encode()

		cipherText = cipherData(pad(data),key)
		print(f"the cipher text is : {cipherText.hex()}")


	if choice == '2':

		cipherText = input("enter cipherText : ")

		cipherText = bytearray.fromhex(cipherText)

		clear = decipherData(cipherText,key)
		unpadClear = unpad(clear)

		recoveredUsername = unpadClear[-32:] 
		print(f"your username is : {recoveredUsername}")

	if choice == '3':
		exit()

