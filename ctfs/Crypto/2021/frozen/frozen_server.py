#!/usr/bin/env python3

from Crypto.Util.number import *
from gmpy2 import *
import sys, random, string
from flag import FLAG

def genrandstr(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N))

def paramaker(nbit):
	p = getPrime(nbit)
	r = getRandomRange(1, p)
	return p, r

def keygen(params, l, d):
	p, r = params
	s = getRandomRange(1, p)
	U = [pow(r, c + 1, p) * s % p for c in range(0,l)]
	V = [int(bin(u)[2:][:-d] + '0' * d, 2) for u in U]
	S = [int(bin(u)[2:][-d:], 2) for u in U]
	privkey, pubkey = S, V
	return pubkey, privkey

def sign(msg, privkey, d):
	msg = msg.encode('utf-8')
	l = len(msg) // 4
	M = [bytes_to_long(msg[4*i:4*(i+1)]) for i in range(l)]
	q = int(next_prime(max(M)))
	sign = [M[i]*privkey[i] % q for i in range(l)]
	return sign

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
	pr(border, " hi young cryptographers, welcome to the frozen signature battle!!  ", border)
	pr(border, " Your mission is to forge the signature for a given message, ready?!", border)
	pr(border*72)

	randstr = genrandstr(20)
	nbit, dbit = 128, 32
	params = paramaker(nbit)
	l = 5
	pubkey, privkey = keygen(params, l, dbit)

	while True:
		pr("| Options: \n|\t[S]how the params \n|\t[P]rint pubkey \n|\t[E]xample signature \n|\t[F]orge the signature \n|\t[Q]uit")
		ans = sc().lower()
		if ans == 's':
			pr(f'| p = {params[0]}')
			pr(f'| r = {params[1]}')
		elif ans == 'p':
			pr(f'pubkey = {pubkey}')
		elif ans == 'e':
			pr(f'| the signature for "{randstr}" is :')
			pr(f'| signature = {sign(randstr, privkey, dbit)}')
		elif ans == 'f':
			randmsg = genrandstr(20)
			pr(f'| send the signature of the following message like example: {randmsg}')
			SIGN = sc()
			try:
				SIGN = [int(s) for s in SIGN.split(',')]
			except:
				die('| your signature is not valid! Bye!!')
			if SIGN == sign(randmsg, privkey, dbit):
				die(f'| Congrats, you got the flag: {FLAG}')
			else:
				die(f'| Your signature is not correct, try later! Bye!')
		elif ans == 'q':
			die("Quitting ...")
		else:
			die("Bye ...")

if __name__ == '__main__':
	main()