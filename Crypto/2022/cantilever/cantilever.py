#!/usr/bin/env python3

from Crypto.Util.number import *
from flag import flag

def gen_primes(nbit, imbalance):
	p = 2
	FACTORS = [p]
	while p.bit_length() < nbit - 2 * imbalance:
		factor = getPrime(imbalance)
		FACTORS.append(factor)
		p *= factor
	rbit = (nbit - p.bit_length()) // 2

	while True:
		r, s = [getPrime(rbit) for _ in '01']
		_p = p * r * s
		if _p.bit_length() < nbit: rbit += 1
		if _p.bit_length() > nbit: rbit -= 1
		if isPrime(_p + 1):
			FACTORS.extend((r, s))
			p = _p + 1
			break

	FACTORS.sort()
	return (p, FACTORS)

def genkey(nbit, imbalance, e):
	while True:
		p, FACTORS = gen_primes(nbit // 2, imbalance)
		if len(FACTORS) != len(set(FACTORS)):
			continue
		q, q_factors = gen_primes(nbit // 2, imbalance + 1)
		if len(q_factors) != len(set(q_factors)):
			continue
		factors = FACTORS + q_factors
		if e not in factors:
			break
	n = p * q
	return n, (p, q)

nbit = 2048
imbalance = 19
e = 0x10001

m_1 = bytes_to_long(flag[:len(flag) // 2])
m_2 = bytes_to_long(flag[len(flag) // 2:])

n, PRIMES = genkey(nbit, imbalance, e)

c_1 = pow(m_1, e, n)
c_2 = pow(e, m_2, n)

print(f'n = {n}')
print(f'c_1 = {c_1}')
print(f'c_2 = {c_2}')