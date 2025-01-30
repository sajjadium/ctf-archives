#!/usr/bin/env python3

from Crypto.Util.number import getPrime, bytes_to_long as btl, inverse
from secrets import randbits
from nttmul import conv
from SECRET import FLAG
import signal

TIMEOUT = 30

B = 7639 # chosen by fair dice roll

def fromPoly(arr):
	num = 0
	for idx in reversed(range(len(arr))):
		num *= B
		num += arr[idx]
	
	return num

def toPoly(num):
	arr = []
	while num != 0:
		num, tmp = divmod(num, B)
		arr.append(tmp)

	return arr

def multiply(a: int, b: int) -> int:
	aPoly = toPoly(a)
	bPoly = toPoly(b)
	cPoly = conv(aPoly, bPoly)
	return fromPoly(cPoly)

def modpow(base: int, ex: int, mod: int) -> int:
	ret = 1
	while ex:
		if ex & 1 == 1:
			ret = multiply(ret, base)
			ret %= mod
		base = multiply(base, base)
		base %= mod
		ex >>= 1
	
	return ret

def encrypt(p: int, q: int, e: int, data: int) -> int:
	encp = modpow(data % p, e, p)
	encq = modpow(data % q, e, q)
	pInvQ = inverse(p, q)
	qInvP = inverse(q, p)

	return (encp * qInvP * q + encq * pInvQ * p) % (p * q)


if __name__ == '__main__':	
	p = getPrime(512)
	q = getPrime(512)
	N = p * q
	e = 0x10001
	FLAG = btl(FLAG)
	signal.alarm(TIMEOUT)
	print('### FASTCRYPTO ###')
	print(f'{N = }')
	while True:
		print('1. Get flag\n2. Encrypt data\n3. Exit')
		choice = input('choice: ')
		assert choice == '1' or choice == '2' or choice == '3'
		if choice == '1':
			data = randbits(1024)
			enc = encrypt(p, q, e, data)
			print(f'{enc = }')
			decryptedData = int(input('pt: '))
			assert data == decryptedData

			enc = encrypt(p, q, e, FLAG)
			print(f'{enc = }')
		elif choice == '2':
			data = randbits(1024)
			print(f'{data = }')
			enc = encrypt(p, q, e, data)
			print(f'{enc = }')
		else:
			exit()
