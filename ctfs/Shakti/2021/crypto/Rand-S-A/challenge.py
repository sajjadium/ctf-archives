import random
from Crypto.Util.number import *
from secret import flag, x

mod = 124912888168404777121624746046278221478415741204063939426455884264204774777990089137717126267769
g = 3
h = pow(g,x,mod)


def keyGen(x):
	random.seed(x)
	p = random.randint(2**511,2**512 - 1)
	while isPrime(p) != 1:
		p = random.randint(2**511,2**512 - 1)

	q = random.randint(2**511,2**512 - 1)
	while isPrime(q) != 1 and q != p:
		q = random.randint(2**511,2**512 - 1)

	e = 65537
	phin = (p-1)*(q-1)
	if GCD(e,phin) == 1:
		return p,q



p,q = keyGen(x)
n = p*q
e = 65537
flag = bytes_to_long(flag)
ct = pow(flag,e,n)


print("g: " + str(g))
print("h: " + str(h))
print "n: " + str(n)
print "ct: " + str(ct)
