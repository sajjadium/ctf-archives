from AES import encrypt, decrypt, padding
from binascii import hexlify, unhexlify
from hashlib import md5
import os

flag = b"XXXXXX"
msg = b"here_is_my_code!"
keys = [ b'XXXXXXXXXXXXXXXX', b'XXXXXXXXXXXXXXXX' ]

g = 41899070570517490692126143234857256603477072005476801644745865627893958675820606802876173648371028044404957307185876963051595214534530501331532626624926034521316281025445575243636197258111995884364277423716373007329751928366973332463469104730271236078593527144954324116802080620822212777139186990364810367977
p = 174807157365465092731323561678522236549173502913317875393564963123330281052524687450754910240009920154525635325209526987433833785499384204819179549544106498491589834195860008906875039418684191252537604123129659746721614402346449135195832955793815709136053198207712511838753919608894095907732099313139446299843
private_key = 0 # Alice Private Key


def main():
	public_key = pow(g, private_key, p)
	print("> Here is my public key: {}".format(public_key))
	key = int(input("> Your public key: "))

	if(key == 0 or key == 1 or key == p - 1):
		print("> Ohhh...... Weak Keys")
		exit(0)

	aes_key = md5(unhexlify(hex(pow(key, private_key, p))[2:])).digest()
	keys.append(aes_key)
	encrypted_msg = encrypt(msg, keys, b"A"*16, b"B"*16)
	encrypted_flag = encrypt(flag[:32], keys, b"A"*16, b"B"*16)
	print("> Your output: {} {}".format(hexlify(encrypted_msg), hexlify(encrypted_flag)))

if __name__ == '__main__':
	main()