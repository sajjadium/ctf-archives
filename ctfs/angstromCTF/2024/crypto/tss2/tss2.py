#!/usr/local/bin/python

from hashlib import sha256
import fastecdsa.curve
import fastecdsa.keys
import fastecdsa.point

TARGET = b'flag'

curve = fastecdsa.curve.secp256k1

def input_point():
	x = int(input('x: '))
	y = int(input('y: '))
	return fastecdsa.point.Point(x, y, curve=curve)

def input_sig():
	c = int(input('c: '))
	s = int(input('s: '))
	return (c, s)

def hash_transcript(pk, R, msg):
	h = sha256()
	h.update(f'({pk.x},{pk.y})'.encode())
	h.update(f'({R.x},{R.y})'.encode())
	h.update(msg)
	return int.from_bytes(h.digest(), 'big') % curve.q

def verify(pk, msg, sig):
	c, s = sig
	R = s * curve.G + c * pk
	return c == hash_transcript(pk, R, msg)

if __name__ == '__main__':
	import sys

	if len(sys.argv) == 2 and sys.argv[1] == 'setup':
		sk1, pk1 = fastecdsa.keys.gen_keypair(curve)
		with open('key.txt', 'w') as f:
			f.write(f'{sk1}\n{pk1.x}\n{pk1.y}\n')
		exit()

	with open('key.txt') as f:
		sk1, x, y = map(int, f.readlines())
		pk1 = fastecdsa.point.Point(x, y, curve=curve)

	print(f'my public key: {(pk1.x, pk1.y)}')

	print('gimme your public key')
	pk2 = input_point()

	print('prove it!')
	sig = input_sig()
	if not verify(pk2, b'foo', sig):
		print('boo')
		exit()

	apk = pk1 + pk2
	print(f'aggregate public key: {(apk.x, apk.y)}')

	print('what message do you want to sign?')
	msg = bytes.fromhex(input('message: '))
	if msg == TARGET:
		print('anything but that')
		exit()

	k1, R1 = fastecdsa.keys.gen_keypair(curve)
	print(f'my nonce: {(R1.x, R1.y)}')

	print(f'gimme your nonce')
	R2 = input_point()

	R = R1 + R2
	print(f'aggregate nonce: {(R.x, R.y)}')

	c = hash_transcript(apk, R, msg)
	s = (k1 - c * sk1) % curve.q
	print(f'my share of the signature: {s}')

	print(f'gimme me the aggregate signature for "{TARGET}"')
	sig = input_sig()
	if verify(apk, TARGET, sig):
		with open('flag.txt') as f:
			flag = f.read().strip()
			print(flag)
