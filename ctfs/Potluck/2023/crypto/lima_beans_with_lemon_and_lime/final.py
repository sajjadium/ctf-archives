#!/usr/bin/env python3

from Crypto.Util.number import getPrime, bytes_to_long
from secrets import randbelow, randbits
from FLAG import flag

beanCount = 8
beanSize = 2048
lemonSize = beanSize // 2 * beanCount
killerBean = getPrime(beanSize)
queries = 17

def pkcs16(limaBeans):
	filledLimaBeans = [0 for _ in range(beanCount)]
	limaBeans += b'A' * ((beanCount * beanSize // 8) - len(limaBeans))
	cookedLimaBeans = bytes_to_long(limaBeans)
	for idx in range(beanCount):
		cookedLimaBeans, filledLimaBeans[idx] = divmod(cookedLimaBeans, killerBean)
	return filledLimaBeans

def encrypt(limaBeans, lemon, lime):
	limaBeansWithLemonAndLime = 0
	for idx in range(beanCount):
		lemonSlice = lemon[idx]
		limaBean = limaBeans[idx]
		if (lime >> idx) & 1:
			limaBean **= 2
			limaBean %= killerBean
		limaBeansWithLemonAndLime += limaBean * lemonSlice
		limaBeansWithLemonAndLime %= killerBean	

	return limaBeansWithLemonAndLime

flag = pkcs16(flag)
print(f'Hello and welcome to the lima beans with lemon and lime cryptosystem. It it so secure that it even has a {lemonSize} bit encryption key, that is {lemonSize // 256} times bigger than an AES-256, and therefore is {lemonSize // 256} times more secure')
print(f'p: {killerBean}')
for turn in range(queries):
	print('1: Encrypt a message\n2: Encrypt flag\n3: Decrypt message')
	choice = input('> ')
	if choice not in ('1', '2', '3'):
		print('What?')
	if choice == '1':
		limaBeans = input('msg: ').encode()
		if len(limaBeans) * 8 > beanSize * beanCount:
			print('Hmmm a bit long innit?')
			continue
		limaBeans = pkcs16(limaBeans)
		lemon = [randbelow(2**(beanSize - 48)) for _ in range(beanCount)]
		lime = randbits(beanCount)
		limaBeansWithLemonAndLime = encrypt(limaBeans, lemon, lime)
		print(f'ct: {limaBeansWithLemonAndLime}')
		print(f'iv: {lime}')
		print(f'key: {",".join(map(str, lemon))}')
	elif choice == '2':
		lemon = [randbelow(2**(beanSize//2)) for _ in range(beanCount)]
		lime = randbits(beanCount)
		limaBeansWithLemonAndLime = encrypt(flag, lemon, lime)
		print(f'ct: {limaBeansWithLemonAndLime}')
		print(f'iv: {lime}')
		print(f'key: {",".join(map(str, lemon))}')
	else:
		print('patented, sorry')
