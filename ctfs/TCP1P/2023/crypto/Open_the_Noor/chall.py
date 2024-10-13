from Crypto.Cipher import AES
import os
import random
import string

CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
KEY = os.urandom(16)

class Systems:
	def __init__(self):
		self.adminpass = self.gen_password()

	def pad(self, s):
	    return s + (16 - len(s) % 16) * chr(16 - len(s) % 16).encode()

	def unpad(self, pt):
	    pad_length = pt[-1]
	    if not 1 <= pad_length <= 16:
	        return None
	    if self.pad(pt[:-pad_length]) != pt:
	        return None
	    return pt[:-pad_length]

	def encryption(self, msg):
		iv = os.urandom(16)
		cipher = AES.new(KEY, AES.MODE_CBC, iv=iv)
		return (iv + cipher.encrypt(msg)).hex()

	def decryption(self, msg):
		msg = bytes.fromhex(msg)
		ivnya = msg[:16]
		msg = msg[16:]
		cipher = AES.new(KEY, AES.MODE_CBC, iv=ivnya)
		return self.unpad(cipher.decrypt(msg))

	def gen_password(self):
		return ''.join([random.choice(CHARSET)for i in range(40)]).encode()

	def secured_password(self):
		return self.encryption(self.pad(self.adminpass))

def main():
	print('You are connected to:')
	print('=====================')
	print('   The Sacred Noor   ')
	print('=====================')
	systems = Systems()
	while True:
		try:
			print("")
			print("1. Login as Admin")
			print("2. Forgot password")
			print("3. Retrieve Encrypted Password")
			print("4. Exit")
			choice = input("> ")
			if choice == "1":
				print("Enter Admin Encrypted Password")
				userpass = input("[?] ")
				check = systems.decryption(userpass)
				if check != None:
					if check == b"nottheflagbutstillcrucialvalidation":
						print("Logged In!")
						print("Here's your flag: TCP1P{REDACTED}")
					else:
						print("[!] INTRUDER ALERT")
				else:
					print("[!] Something's wrong.")
			elif choice == "2":
				systems.adminpass = systems.gen_password()
				print("Password Changed!")
			elif choice == "3":
				print("Secured Password")
				print("[+]", systems.secured_password())
			elif choice == "4":
				print("Bye then.")
				break
			else:
				print("Bzz error")
				exit()
		except:
			print("[!] Something's wrong.")

if __name__ == '__main__':
	main()
