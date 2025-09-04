from Crypto.PublicKey import RSA
from Crypto.Cipher import AES

flag = open('flag.txt','r').read().strip().encode()
pad = (16 - len(flag)) % 16
flag = flag + pad * int(16).to_bytes()

key = RSA.generate(2048, e = 1337)
n = key.n
e = key.e
d = key.d

AES_key = int(bin(d)[2:258:2],2).to_bytes(16)
crypter = AES.new(AES_key, AES.MODE_ECB)
cipher = crypter.encrypt(flag)
print(cipher.hex())

for _ in range(128):
	user_input = input('(e)ncrypt|(d)ecrypt:<number>\n')
	option,m = user_input.split(':')
	m = int(m)
	if option == 'e':
		print(pow(m,e,n))
	elif option == 'd':
		print(pow(m,d,n))
	else:
		print('wrong option')
