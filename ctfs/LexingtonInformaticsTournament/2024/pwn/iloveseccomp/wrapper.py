#!/usr/bin/env python3
from os import urandom
import pwn
from time import sleep

def init():
	key = urandom(8)
	with open("key.txt", "wb") as f:
		f.write(key)
	return key

def prog():
	r = pwn.process("./main")
	sleep(0.5)
	print(r.recvS())

	try:
		payload = bytes.fromhex(input())
	except:
		print("my guy")
		exit(0)
	r.sendline(payload)
	sleep(0.5)
	print(f"Process exited with code {r.poll()}")

def check(key):
	userKey = bytes.fromhex(input("Okay... WHAT IS THE KEY (in hex) "))
	if userKey == key:
		print("Lucky guess...")
		with open("flag.txt", "r") as f:
			print(f.read())
	else:
		print("nope")

if __name__ == '__main__':
	print("***The program will run eight times***\n")
	key = init()
	for _ in range(8):
		prog()
	check(key)
