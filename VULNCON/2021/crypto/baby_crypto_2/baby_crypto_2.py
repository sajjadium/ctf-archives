from hashlib import sha1
from os import urandom

from Crypto.Util.number import bytes_to_long, getPrime
from collections import namedtuple
from textwrap import dedent

DIFFICULTY = 20

PubKey = namedtuple("PubKey", "p q g")
privkey = bytes_to_long(b"REDACTED")


class LCG:
	def __init__(self, m: int, a: int, b: int) -> None:
		self.m = m
		self.a = a
		self.b = b
		self.s = bytes_to_long(urandom(DIFFICULTY)) | 1

		while self.a >= self.m:
			self.a = bytes_to_long(urandom(DIFFICULTY)) | 1

		while self.b >= self.m:
			self.b = bytes_to_long(urandom(DIFFICULTY)) | 1

	def seed(self) -> None:
		self.s = bytes_to_long(urandom(DIFFICULTY)) | 1

	def getRandom(self) -> int:
		self.s = (self.a * self.s + self.b) % self.m
		return self.s

	def help(self) -> None:
		print(
		    dedent(f"""
			LCG HELP ->
			This generates random numebrs like so -
			{self.getRandom()}
			{self.getRandom()}
			{self.getRandom()}
			{self.getRandom()}
			See, completely random :)
		"""))
		self.seed()


def sign(pubkey: PubKey, x: int, h: int, k: int):
	p, q, g = pubkey
	r = pow(g, k, p) % q
	s = (pow(k, -1, q) * (h + x * r)) % q
	return r, s


def printSignatures(lcg: LCG, pub: PubKey, priv: int) -> None:
	msgs = [b"Hello", b"there"]
	hashes = [bytes_to_long(sha1(m).digest()) for m in msgs]
	nonces = [lcg.getRandom() for _ in hashes]
	signs = [sign(pub, priv, h, k) for h, k in zip(hashes, nonces)]
	print("\n".join(f"sign_{i} = {sign}" for i, sign in enumerate(signs)))


m = getPrime(DIFFICULTY * 8)
a = bytes_to_long(urandom(DIFFICULTY)) | 1
b = bytes_to_long(urandom(DIFFICULTY)) | 1
pubkey = PubKey(
    7723227163652206196072315877851665970492409383498621787915763836703165497532056144920977718337221463593649391334584803149362349291402576071382757173855489,
    1419435951773960878522380192164715964887544050251,
    3177589275498063000838438765591095514446952503023627047492796256311729225229378235819032575431223841654220960177156277529073194075117755794549781574237012
)
# sanity check
if privkey > pubkey.q:
	print("WTF. Contact admin")
	exit()

lcg = LCG(m, a, b)
lcg.help()
print("BTW, I made some spicy signatures with that LCG ->")
printSignatures(lcg, pubkey, privkey)
print("Please use them carefully")

"""
LCG HELP ->
This generates random numebrs like so -
571950745479432267005464851096356774896792314093
442389987284185335289253341364665422032816391623
674689295937843496428836795727103849648022363056
534115548763794721117336167251846846861246743872
See, completely random :)

BTW, I made some spicy signatures with that LCG ->
sign_0 = (1068578444686700850472665790275239904755324934637, 773641167123158554564050069711067502164705010631)
sign_1 = (1261138445303763427942699370178218831470626347614, 466653063468278381121557045661962018351821473529)
Please use them carefully
"""
