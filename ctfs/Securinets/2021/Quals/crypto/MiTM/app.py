from Crypto.Util.number import long_to_bytes
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from secret import flag
import hashlib, random, os
import signal

class DHx():
	def __init__(self):
		self.g = 2
		self.p = 0xf18d09115c60ea0e71137b1b35810d0c774f98faae5abcfa98d2e2924715278da4f2738fc5e3d077546373484585288f0637796f52b7584f9158e0f86557b320fe71558251c852e0992eb42028b9117adffa461d25c8ce5b949957abd2a217a011e2986f93e1aadb8c31e8fa787d2710683676f8be5eca76b1badba33f601f45		
		self.private = random.randint(1, self.p-1)
		self.secret = None

	def getPublicKey(self):
		return pow(self.g, self.private, self.p)

	def share(self, x : int):
		assert x > 1 and x < self.p
		return pow(x, self.private, self.p)

	def getSharedSecret(self, x : int):
		assert x > 1 and x < self.p
		self.secret = pow(x, self.private, self.p)

	def getFingerprint(self):
		return hashlib.sha256(long_to_bytes(self.secret)).hexdigest()

	def checkFingerprint(self, h1 : str, h2 : str ):
		return h1 == h2 == self.getFingerprint()

	def encryptFlag(self):
		iv = os.urandom(16)
		key = hashlib.sha1(long_to_bytes(self.secret)).digest()[:16]
		return iv.hex() + AES.new(key, AES.MODE_CBC, iv).encrypt(pad(flag, 16)).hex()

signal.alarm(60)

Alice = DHx()
Bob = DHx()
Carol = DHx()

A = Alice.getPublicKey()
print("Alice sends to Bob: {}".format(A))
A = int(input("Forward to Bob: "))
B = Bob.share(A)
print("Bob sends to Carol: {}".format(B))
B = int(input("Forward to Carol: "))
Carol.getSharedSecret(B)

B = Bob.getPublicKey()
print("Bob sends to Carol: {}".format(B))
B = int(input("Forward to Carol: "))
C = Carol.share(B)
print("Carol sends to Alice: {}".format(C))
C = int(input("Forward to Alice: "))
Alice.getSharedSecret(C)

C = Carol.getPublicKey()
print("Carol sends to Alice: {}".format(C))
C = int(input("Forward to Alice: "))
A = Alice.share(C)
print("Alice sends to Bob: {}".format(A))
A = int(input("Forward to Bob: "))
Bob.getSharedSecret(A)

print ("Alice says: ")
if (Alice.checkFingerprint(Carol.getFingerprint(), Bob.getFingerprint())):
	print (Alice.encryptFlag())
else:
	print ("ABORT MISSION! Walls have ears; Be careful what you say as people may be eavesdropping.")