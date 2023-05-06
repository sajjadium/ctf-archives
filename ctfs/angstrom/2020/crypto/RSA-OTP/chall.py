from Crypto.Util.number import bytes_to_long
from Crypto.Random.random import getrandbits # cryptographically secure random get pranked
from Crypto.PublicKey import RSA
from secret import d, flag
# 1024-bit rsa is unbreakable good luck
n = 136018504103450744973226909842302068548152091075992057924542109508619184755376768234431340139221594830546350990111376831021784447802637892581966979028826938086172778174904402131356050027973054268478615792292786398076726225353285978936466029682788745325588134172850614459269636474769858467022326624710771957129
e = 0x10001
key = RSA.construct((n,e,d))

f = bytes_to_long(bytes(flag,'utf-8'))
print("Encrypted flag:")
print(key.encrypt(f,0)[0])

def otp(m):
	# perfect secrecy ahahahaha
	out = ""
	for i in bin(m)[2:]:
		out+=str(int(i)^getrandbits(1))
	return out

while 1:
	try:
		i = int(input("Enter message to sign: "))
		assert(0 < i < n)
		print("signed message (encrypted with unbreakable otp):")
		print(otp(key.decrypt(i)))
	except:
		print("bad input, exiting")
		break