import secrets
import sympy

FLAG="crew{fake_flag}"
BITS=512
LIM=pow(2,BITS)

while True:
	while (not sympy.isprime(p:=secrets.randbelow(LIM//2)+LIM//2)) or (p-1)%3==0:
		pass

	while (not sympy.isprime(q:=secrets.randbelow(LIM//2)+LIM//2)) or (q-1)%3==0:
		pass

	n=p*q
	if n>pow(2,1023):
		break

phi=(p-1)*(q-1)
e=3
Secret=secrets.randbelow(LIM)
d=pow(e,-1,phi)
sig=pow(Secret,d,n)

print("The signature is: "+str(sig))

def hamming_weight(x):
	return sum([int(y) for y in bin(x)[2:]])


while True:
	print("I can encrypt anything for you! But the bits may get messy")
	msg=input()
	if msg=="guess":
		print("Do you know the secret?")
		msg=int(input())
		if msg==Secret:
			print("You sure do! Here is your prize:")
			print(FLAG)
			exit(0)
		else:
			print("Wrong answer!")
			exit(0)
	msg=int(msg)
	enc=pow(msg,3,n)
	print(hamming_weight(enc)%2)



