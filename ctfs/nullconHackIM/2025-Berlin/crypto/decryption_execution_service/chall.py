from Crypto.Cipher import AES
import os
import json

class PaddingError(Exception):
	pass

flag = open('flag.txt','r').read().strip()
key = os.urandom(16)

def unpad(msg : bytes):
	pad_byte = msg[-1]
	if pad_byte == 0 or pad_byte > 16: raise PaddingError
	for i in range(1, pad_byte+1):
		if msg[-i] != pad_byte: raise PaddingError
	return msg[:-pad_byte]

def decrypt(cipher : bytes):
	if len(cipher) % 16 > 0: raise PaddingError
	decrypter = AES.new(key, AES.MODE_CBC, iv = cipher[:16])
	msg_raw = decrypter.decrypt(cipher[16:])
	return unpad(msg_raw)

if __name__ == '__main__':
	while True:
		try:
			cipher_hex = input('input cipher (hex): ')
			if cipher_hex == 'exit': break
			cipher = decrypt(bytes.fromhex(cipher_hex))
			json_token = json.loads(cipher.decode())
			eval(json_token['command'])
		except PaddingError:
			print('invalid padding')
		except (json.JSONDecodeError, UnicodeDecodeError):
			print('no valid json')
		except:
			print('something else went wrong')
