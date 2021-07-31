#!/usr/bin/python3

from Crypto.Util.number import *
from gmpy2 import *
from secret import *
from flag import flag

global nbit
nbit = 1024

def keygen(nbit):
	while True:
		p, q = [getStrongPrime(nbit) for _ in '01']
		if p % 4 == q % 4 == 3:
			return (p**2)*q, p

def encrypt(m, pubkey):
	if GCD(m, pubkey) != 1 or m >= 2**(2*nbit - 2):
		return None
	return pow(m, 2, pubkey)

def flag_encrypt(flag, p, q):
	m = bytes_to_long(flag)
	assert m < p * q
	return pow(m, 65537, p * q)

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
	pr(border, "  hi all, welcome to Rooney Oracle, you can encrypt and decrypt any ", border)
	pr(border, "  message in this oracle, but the flag is still encrypted, Rooney   ", border)
	pr(border, "  asked me to find the encrypted flag, I'm trying now, please help! ", border)
	pr(border*72)

	pubkey, privkey = keygen(nbit)
	p, q = privkey, pubkey // (privkey ** 2)

	while True:
		pr("| Options: \n|\t[E]ncrypt message \n|\t[D]ecrypt ciphertext \n|\t[S]how encrypted flag \n|\t[Q]uit")
		ans = sc().lower()
		if ans == 'e':
			pr("| Send the message to encrypt: ")
			msg = sc()
			try:
				msg = int(msg)
			except:
				die("| your message is not integer!!")
			pr(f"| encrypt(msg, pubkey) = {encrypt(msg, pubkey)} ")
		elif ans == 'd':
			pr("| Send the ciphertext to decrypt: ")
			enc = sc()
			try:
				enc = int(enc)
			except:
				die("| your message is not integer!!")
			pr(f"| decrypt(enc, privkey) = {decrypt(enc, privkey)} ")
		elif ans == 's':
			pr(f'| enc = {flag_encrypt(flag, p, q)}')
		elif ans == 'q':
			die("Quitting ...")
		else:
			die("Bye ...")

if __name__ == '__main__':
	main()