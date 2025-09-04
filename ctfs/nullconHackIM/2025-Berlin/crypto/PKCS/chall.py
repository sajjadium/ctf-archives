from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

BIT_LEN = 1024

k = RSA.generate(BIT_LEN, e = 3)
flag = open('flag.txt','r').read().encode()

encrypter = PKCS1_v1_5.new(k)
cipher1 = encrypter.encrypt(flag).hex()
cipher2 = encrypter.encrypt(flag).hex()

print(len(flag))
print(k.n)
print(cipher1)
print(cipher2)
