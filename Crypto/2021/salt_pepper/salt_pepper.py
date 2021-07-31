#!/usr/bin/env python3

from hashlib import md5, sha1
import sys
from secret import salt, pepper
from flag import flag

assert len(salt) == len(pepper)	== 19
assert md5(salt).hexdigest()	== '5f72c4360a2287bc269e0ccba6fc24ba'
assert sha1(pepper).hexdigest()	== '3e0d000a4b0bd712999d730bc331f400221008e0'

def auth_check(salt, pepper, username, password, h):
	return sha1(pepper + password + md5(salt + username).hexdigest().encode('utf-8')).hexdigest() == h

def die(*args):
	pr(*args)
	quit()

def pr(*args):
	s = " ".join(map(str, args))
	sys.stdout.write(s + "\n")
	sys.stdout.flush()

def sc():
	return sys.stdin.readline().strip()

def main():
	border = "+"
	pr(border*72)
	pr(border, "  welcome to hash killers battle, your mission is to login into the ", border)
	pr(border, "  ultra secure authentication server with provided information!!    ", border)
	pr(border*72)

	USERNAME = b'n3T4Dm1n'
	PASSWORD = b'P4s5W0rd'

	while True:
		pr("| Options: \n|\t[L]ogin to server \n|\t[Q]uit")
		ans = sc().lower()
		if ans == 'l':
			pr('| send your username, password as hex string separated with comma: ')
			inp = sc()
			try:
				inp_username, inp_password = [bytes.fromhex(s) for s in inp.split(',')]
			except:
				die('| your input is not valid, bye!!')
			pr('| send your authentication hash: ')
			inp_hash = sc()
			if USERNAME in inp_username and PASSWORD in inp_password:
				if auth_check(salt, pepper, inp_username, inp_password, inp_hash):
					die(f'| Congrats, you are master in hash killing, and it is the flag: {flag}')
				else:
					die('| your credential is not valid, Bye!!!')
			else:
				die('| Kidding me?! Bye!!!')
		elif ans == 'q':
			die("Quitting ...")
		else:
			die("Bye ...")

if __name__ == '__main__':
	main()