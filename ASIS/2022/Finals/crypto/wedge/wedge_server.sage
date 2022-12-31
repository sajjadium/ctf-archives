#!/usr/bin/env sage

import sys
from secret import decrypt, flag

def random_vec(k, B):
	Zn = Zmod(B)
	return [Zn(randint(0, B-1)) for _ in range(k)]

def genkey(k, n):
	while True:
		uv = [random_vec(k, n) for _ in '01']
		A, B = [matrix([uv[_][-l:] + [0]*(k-l) for l in range(1, k + 1)]) for _ in range(2)]
		if gcd(A[0][0], n) == gcd(B[0][0], n) == 1:
			N = matrix([random_vec(k, n) for _ in range(k)])
			if gcd(det(N), n) == 1 and N[0][-1] > 0:
				rN = (A * B**2).inverse() * N * (A * B**2)
				sN = (B * A**2).inverse() * N.inverse() * (B * A**2)
				pkey = (n, rN, sN)
				skey = (A, B)
				return pkey, skey

def msg2mat(m, pkey):
	n, rN, sN = pkey
	k, Zn = len(rN[0]), Zmod(n)
	assert len(m) <= k ** 2
	m = m + (k**2 - len(m)) * '='
	_m = list(m)
	M = matrix(Zn, [list(map(ord, _m[i*k:(i+1)*k])) for i in range(0, k)])
	return M

def encrypt(M, pkey):
	n, rN, sN = pkey
	k, Zn = len(rN[0]), Zmod(n)
	assert len(M[0]) <= k
	r = list(M[0])
	while True:
		if gcd(r[-1], n) == 1:
			RM = matrix(Zn, [r[-l:] + [0]*(k-l) for l in range(1, k + 1)])
			C1 = RM * sN * RM.inverse()
			C2 = M * RM * rN * RM.inverse()
			return (C1, C2)
		else: 
			r = random_vec(k, n)

def die(*args):
	pr(*args)
	quit()

def pr(*args):
	s = " ".join(map(str, args))
	sys.stdout.write(s + "\n")
	sys.stdout.flush()

def sc():
	return sys.stdin.buffer.readline()

def main():
	border = "|"
	pr(border*72)
	pr(border, "Hi all, now it's time to break a relatively tough challenge about   ", border)
	pr(border, "matrices! We will generate key pair and decrypt given message, also ", border)
	pr(border, "you are able to decrypt some ciphertexts too!                       ", border)
	pr(border*72)

	k, n = randint(11, 19), 126
	Zn = Zmod(n)
	pkey, skey = genkey(k, n)
	A, B = skey
	n, rN, sN = pkey

	while True:
		pr(border, "Options: \n|\t[E]ncrypted flag! \n|\t[D]ecrypt ciphertext \n|\t[P]ublic key \n|\t[Q]uit")
		ans = sc().decode().lower().strip()
		m = msg2mat(flag, pkey)
		C = encrypt(m, pkey)
		C1, C2 = C
		if ans == 'e':
			pr(border, f'C1 = {C1}')
			pr(border, f'C2 = {C2}')
		elif ans == 'd':
			pr(border, f"Please send your ciphertext matrix as an 1 x {k**2} array separated by comma.")
			pr(border, f"First send C1: ")
			_C1 = sc().decode().strip()
			pr(border, f"Now send C2: ")
			_C2 = sc().decode().strip()
			try:
				_C1 = [Zn(_) for _  in _C1.split(',')]
				_C2 = [Zn(_) for _  in _C2.split(',')]
				if len(_C1) == len(_C2) == k**2:
					_C1 = [_C1[i*k:(i+1)*k] for i in range(k)]
					_C2 = [_C2[i*k:(i+1)*k] for i in range(k)]
					_C1 = matrix(_C1)
					_C2 = matrix(_C2)
					if _C1 == C1 and _C2 == C2:
						die(border, 'Kidding me! Bye!!')
				else:
					die(border, 'Exception! Bye!!')
			except:
				die(border, 'Your input is not valid! Bye!!')
			_C = (_C1, _C2)
			msg = decrypt(_C, A, B)
			pr(border, f'The plaintext is:\n {msg}')
		elif ans == 'p':
			pr(border, f'n = {n}')
			pr(border, f'rN = {rN}')
			pr(border, f'sN = {sN}')
		elif ans == 'q':
			die(border, "Quitting ...")
		else:
			die(border, "Bye ...")

if __name__ == '__main__':
	main()