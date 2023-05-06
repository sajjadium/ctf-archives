from Crypto.Util.number import bytes_to_long, getStrongPrime
from math import gcd
from flag import FLAG
from Crypto.Random import get_random_bytes



def encrypt(m):
    return pow(m,e,N)



e = 65537
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

ct= []

for car in FLAG:
	ct.append(encrypt(car))

print("ct = "+str(ct))
