from Crypto.Util.number import *
from secret import *


assert (x>2 and x%2 == 0)
assert (isPrime(e1) and isPrime(e2))

def functor():
	val1 , val2 = 0,0
	for i in range(x+1):
		val1 += pow(e1,i)
	for j in range(3):
		val2 += pow(e2,j)
	assert (val1 == val2)

def keygen():
	while True:
		p,q = [getStrongPrime(1024) for _ in range(2)]
		if p%4==3 and q%4==3:
			break

	r = 2
	while True:
		r = r*x
		if r.bit_length()>1024 and isPrime(r-1):
			r = r-1
			break

	return p,q,r


functor()
p,q,r = keygen()
n = p*q*r
print(f"p:{p}")
print(f"q:{q}")
ip = inverse(p,q)
iq = inverse(q,p)
c1 = pow(bytes_to_long(flag[0:len(flag)//2].encode('utf-8')),e1,n)
c2 = pow(bytes_to_long(flag[len(flag)//2:].encode('utf-8')),e2,n)
print(f"n:{n}",f"ip:{ip}",f"iq:{iq}",f"c1:{c1}",f"c2:{c2}",sep="\n")












