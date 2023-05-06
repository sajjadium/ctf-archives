#!/usr/local/bin/python

import ctypes

# tar -xf pqov-paper.tar.gz && patch -p1 < patch.diff && make libpqov.so VARIANT=2
libpqov = ctypes.CDLL('./libpqov.so')

CRYPTO_SECRETKEYBYTES = 237912
CRYPTO_PUBLICKEYBYTES = 43576
CRYPTO_BYTES = 128

def sign(sk, m):
	m = ctypes.create_string_buffer(m, len(m))
	mlen = ctypes.c_size_t(len(m))
	sm = ctypes.create_string_buffer(len(m) + CRYPTO_BYTES)
	smlen = ctypes.c_size_t(0)
	libpqov.crypto_sign(sm, ctypes.pointer(smlen), m, mlen, sk)
	return bytes(sm)

def verify(pk, sm):
	assert len(sm) >= CRYPTO_BYTES
	m = ctypes.create_string_buffer(len(sm) - CRYPTO_BYTES)
	mlen = ctypes.c_size_t(0)
	sm = ctypes.create_string_buffer(sm, len(sm))
	smlen = ctypes.c_size_t(len(sm))
	assert libpqov.crypto_sign_open(m, ctypes.pointer(mlen), sm, smlen, pk) == 0
	return bytes(m)

if __name__ == '__main__':
	with open('flag.txt') as f:
		flag = f.read().strip()

	with open('sk.bin', 'rb') as f:
		sk = f.read()

	with open('pk.bin', 'rb') as f:
		pk = f.read()

	print('''\
Welcome to Dice Bistro.

===== SPECIAL MENU =============================================================
Caesar Salad - A mix of greens and seasonal vegetables, tossed in our housemade
    vinaigrette.

Enigma Chicken - A perfectly grilled chicken breast, topped with a drizzle of
    the mysterious vinaigrette, served with a side of potato hash (of course,
    collision-resistant).

Quantum Quinoa Bowl - A delicious combination of quinoa, roasted vegetables,
    and a variety of nuts, all tossed in the mysterious vinaigrette, guaranteed
    to entangle your taste buds.
================================================================================
''')

	order = input('What would you like to order? ').encode()
	if order == b'the vinaigrette recipe':
		print('Only employees of Dice Bistro are allowed to learn the vinaigrette recipe.')
		try:
			sm = bytes.fromhex(input('Authorization: '))
			assert verify(pk, sm) == order
			print(f'Certainly, here it is: {flag}')
		except:
			print('error')
	else:
		sm = sign(sk, order)
		print(f'Certainly, here it is: {sm.hex()}')
