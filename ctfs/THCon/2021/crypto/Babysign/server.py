from Crypto.Util.number import getPrime, GCD, inverse, bytes_to_long
import os

class SecureSigner():
	def __init__(self):
		p = getPrime(512)
		q = getPrime(512)
		e = 0x10001
		phi = (p-1)*(q-1)
		while GCD(e,phi) != 1:
			p = getPrime(512)
			q = getPrime(512)
			phi = (p-1)*(q-1)

		self.d = inverse(e,phi)
		self.n = p * q
		self.e = e

	def sign(self, message):
		return pow(message,self.d,self.n)

	def verify(self, message, signature):
		return pow(signature,self.e,self.n) == message



def menu():
	print(
		"""
		1 - Sign an 8-bit integer
		2 - Execute command
		3 - Exit
		"""
		)
	choice = input("Choice: ")
	if choice == "1":
		try:
			m = int(input("Integer to sign: "))
			if 0 <= m < 256:
				print("Signature: {:d}".format(s.sign(m)))
			else:
				print("You can only sign 8-bit integers.")
		except:
			print("An error occured.")
			exit(1)
	elif choice == "2":
		try:
			cmd = input("Command: ")
			m = bytes_to_long(cmd.encode())
			signature = int(input("Signature: "))
			if s.verify(m,signature):
				os.system(cmd)
			else:
				print("Wrong signature.")
		except:
			print("An error occured.")
			exit(1)
	elif choice == "3":
		exit(0)
	else:
		print("Incorrect input.")
		exit(1)




if __name__ == '__main__':
	s = SecureSigner()

	print("Here are your parameters:\n - modulus n: {:d}\n - public exponent e: {:d}\n".format(s.n, s.e))
	
	while True:
		menu()
	