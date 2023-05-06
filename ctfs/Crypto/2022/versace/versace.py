#!/usr/bin/env python3
# In the name of Allah

from Crypto.Util.number import *
from flag import flag

def keygen(n):
	e = 65537
	x, y = [getRandomRange(2, n - 2) for _ in '01']
	fi = pow(5, x, n)
	th = pow(13, y, n)
	return (n, e, fi, th)

def encrypt(m, pubkey):
	n, e, fi, th = pubkey
	k, u, v = [getRandomRange(2, n - 2) for _ in '012']
	c_1 = pow(k, e, n)
	c_2 = pow(5, u, n)
	c_3 = pow(13, v, n)
	c_4 = pow(fi, u, n) * pow(th, v, n) * pow(k + 1, e, n) * m % n
	return c_1, c_2, c_3, c_4


n = 141886649864474336567180245736091175577519141092893110664440298696325928109107819365023509727482657156444454196974621121317731892910779276975799862237645015028934626195549529415068518701179353407407170273107294065819774663163018151369555922179926003735413019069305586784817562889650637936781439564028325920769
pubkey = keygen(n)
msg = bytes_to_long(flag.encode('utf-8'))
enc = encrypt(msg, pubkey)

print(f'pubkey = {pubkey}')
print(f'enc = {enc}')