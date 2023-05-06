import base64
FLAG = open("flag.txt").readline().strip()

class DialogEncryption:
	def __init__(self, key):
		self.key = key
	
	def encrypt(self, message):
		encoded = ""
		for i in range(len(message)):
			key_c = self.key[i % len(self.key)][::-1]
			encoded_c = chr((ord(message[i]) + ord(key_c)) % 256)
			encoded += encoded_c
		return base64.b64encode(encoded.encode()).decode()
	
	def decrypt(self, message):
		decoded = ""
		message = base64.b64decode(message).decode()
		for i in range(len(message)):
			key_c = self.key[i % len(self.key)][::-1]
			decoded_c = chr((256 + ord(message[i]) - ord(key_c)) % 256)
			decoded += decoded_c
		return decoded

key = FLAG
dialog = DialogEncryption(key)
message = "Hi Alice, I'm Bob. I'm sending you a secret message. I hope you can decrypt it."
encrypted = dialog.encrypt(message)
print(encrypted)
