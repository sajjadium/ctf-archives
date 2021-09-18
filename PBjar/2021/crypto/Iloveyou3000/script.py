import random
from Crypto.Util.number import *

def newflag(oldflag):
	s=list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPWRSTUVWXYYZ")
	for i in range(random.randint(1,10)):
		oldflag=random.choice(s)+oldflag
	for i in range(random.randint(1,10)):
		oldflag=oldflag+random.choice(s)
	return oldflag

with open('flag.txt','r') as f:
    flag = f.read().strip()
    flag=newflag(flag).encode()

m=bytes_to_long(flag)

def cooooolerRandom(x,y):
	base=random.randint(2,5)
	e=base

	operation=random.choice([-1,1]) #subtraction or addition

	_range=random.randint(1,6) #rolling some dice
	change=sum([random.randint(-_range,_range) for i in range(random.randint(1,100))]) #chillllly am I right?
	e*=(x+operation*change)

	operation2=random.choice([-1,1]) #subtraction or addition

	_range=random.randint(1,6) #rolling some more dice
	change2=sum([random.randint(-_range,_range) for i in range(random.randint(1,100))]) #someone get me a blanket pleasee

	
	e*=(y+operation2*change2)
	return e+base,base


print("Weclome to...urr...cool crypto problem thing")
print("We wanted to find out why picking e is sooooo important")
print("Like smh, who needs a good e value???")
print("You know what...I'll show them...I'll give you 3000 different examples on why any e is a good e value!")

example_count=int(input("How many examples do you want?: "))
if (example_count<1 or example_count>3000):
	print("Come on man ;(")
	exit(1)

for i in range(example_count):
	p=getPrime(256)
	q=getPrime(256)
	n=p*q
	assert(m<n)
	e,b=cooooolerRandom(p,q)
	ct=pow(m,e,n)
	print("Ciphertext: "+str(ct))
	print("Modulus: "+str(n))
	print("Base: "+str(b))
