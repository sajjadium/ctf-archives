from Crypto.Util.number import bytes_to_long, getStrongPrime
from math import gcd
from flag import FLAG
from Crypto.Random import get_random_bytes



def encrypt_message(m):
    return pow(m,e,N)


def advanced_encrypt(a,m):
	return encrypt_message(pow(a,3,N)+(m << 24))

e = 3
p = getStrongPrime(512)
q = getStrongPrime(512)


# generate secure keys
result = 0
while (result !=1):
    p = getStrongPrime(512)
    q = getStrongPrime(512)
    result = gcd(e,(p-1)*(q-1)) 	

N = p * q

print("N = " + str(N))
print("e = " + str(e))

rand = bytes_to_long(get_random_bytes(64))

ct = []
ct.append(encrypt_message(rand << 24))

for car in FLAG:
	ct.append(advanced_encrypt(car,rand))

print("ct = "+str(ct))
