from hashlib import sha256
import random, binascii
from os.path import exists

Zx.<x> = ZZ[]
n, q = 167, 128

def convolution(f,g):
	return (f * g) % (x^n-1)

def balancedmod(f,q):
	g = list(((f[i] + q//2) % q) - q//2 for i in range(n))
	return Zx(g) % (x^n-1)

def randomdpoly(d1, d2):
	result = d1*[1]+d2*[-1]+(n-d1-d2)*[0]
	random.shuffle(result)
	return Zx(result)

def invertmodprime(f,p):
	T = Zx.change_ring(Integers(p)).quotient(x^n-1)
	return Zx(lift(1 / T(f)))

def invertmodpowerof2(f,q):
	assert q.is_power_of(2)
	g = invertmodprime(f,2)
	while True:
		r = balancedmod(convolution(g,f),q)
		if r == 1: return g
		g = balancedmod(convolution(g,2 - r),q)

def keypair():
	if exists('key.pub'):
		publickey = Zx(open('key.pub').read())
		secretkey = Zx(open('key.priv').read())
		g = balancedmod(convolution(publickey,invertmodpowerof2(secretkey,q)),q)
	else:
		while True:
			try:
				f = randomdpoly(61, 60)
				f3 = invertmodprime(f,3)
				fq = invertmodpowerof2(f,q)
				break
			except Exception as e:
				pass
		g = randomdpoly(15, 15)
		publickey = balancedmod(3 * convolution(fq,g),q)
		secretkey = f
	return publickey, secretkey, g

def encode(val):
	poly = 0
	for i in range(n):
		c = val % q 
		poly += (((c + q//2) % q) - q//2) * (x^i)
		val //= q
	return poly

def encrypt(message, publickey):
	r = randomdpoly(61, 60)
	return balancedmod(convolution(publickey,r) + message, q), r

def decrypt(ciphertext, secretkey):
	f = secretkey
	f3 = invertmodprime(f,3)
	a = balancedmod(convolution(encode(ciphertext), f), q)
	return balancedmod(convolution(a, f3), 3)

def menu():
	print("\nWhat service would you like?")
	print("\t1. Encrypt a message")
	print("\t2. Decrypt a message")
	print("\t3. Encrypt a secret")
	print("\t4. Quit")

def main():
	publickey, secretkey, _ = keypair()
	while True:
		menu()
		choice = int(input(""))
		if choice == 1:
			print(f"What is the message you would like to encrypt? Please give it in hex format")
			pt = input("")
			if len(pt)%2 == 1:
				pt = '0'+pt
			message = int.from_bytes(binascii.unhexlify(pt), "big")
			print(encrypt(message, publickey))
		elif choice == 2:
			print(f"What is the message you would like to decrypt? Please give it in hex format")
			pt = input("")
			if len(pt)%2 == 1:
				pt = '0'+pt
			ct = int.from_bytes(binascii.unhexlify(pt), "big")
			print(decrypt(ct, secretkey))
		elif choice == 3:
			print(f"What is the secret you would like to encrypt?")
			secret = input("").encode()
			key = int.from_bytes(sha256(str(secretkey).encode()).digest(), "big")
			random.seed(key)
			secret_enc = bytes(a ^^ random.randint(0,255) for a in secret)
			print(secret_enc.hex())
		elif choice == 4:
			break
		else:
			print("Invalid choice. Please try again.")
	
if __name__ == "__main__":
	main()