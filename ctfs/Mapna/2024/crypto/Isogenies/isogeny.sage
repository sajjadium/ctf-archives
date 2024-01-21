#!/usr/bin/env sage

import re
from hashlib import sha256
from secrets import token_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import *
from flag import flag

assert re.match(r"^MAPNA\{.{41}\}", flag.decode())

def to_montgomery(E):
	R = E.base_ring()
	j = E.j_invariant()
	x = polygen(R)
	eq = 256 * (x - 3)**3 - (x - 4) * j
	for A2 in eq.roots(multiplicities=False):
		for A in A2.nth_root(2, all=True):
			Ea = EllipticCurve(R, [0, A, 0, 1, 0])
			if Ea.is_isomorphic(E):
				return Ea

def mask(v, k):
	return int((v >> k) << k)

def main():
	proof.all(False)
	pari.allocatemem(2**30, silent=True)

	h = sha256(flag).digest()
	A = bytes_to_long(h)

	iv = token_bytes(16)
	key = sha256(h).digest()[:16]
	enc = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(flag, 16))
	print(f"iv   = {iv.hex()}")
	print(f"enc  = {enc.hex()}")
	print()

	while True:
		p = getPrime(512)
		E = EllipticCurve(GF(p), [0, A, 0, 1, 0])
		if E.order() % 3 != 0:
			continue

		for _ in range(50):
			P = E.random_point() * (E.order() // 3)
			if P != 0:
				break
		else:
			continue

		Ea = to_montgomery(E.isogeny_codomain(P))
		if Ea is None:
			continue

		A = mask(A, k=64)
		B = mask(Ea.a2(), k=64)
		hint = int(P[0])

		print(f"p    = 0x{p:x}")
		print(f"A    = 0x{A:x}")
		print(f"B    = 0x{B:x}")
		print(f"hint = 0x{hint:x}")

		break

if __name__ == "__main__":
	main()