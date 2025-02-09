#!/usr/bin/env python3
from Crypto.Util.number import *
from Secrets import FLAG

def lmao(n,k,x):  #Better function needed
    pseudo_p = 1 
    for i in range(2,k*n-x):
        try:
            if (GCD(i,n-1)^(n-1)!=0):
                pseudo_p = (pseudo_p*inverse(i,n))%n
        except:
            continue
    return inverse(pseudo_p,n)

e = 27525540

while True:
    p = getPrime(1024)
    if (((15-GCD(e,(p-1)))>>(31))==0):
        break
q = getPrime(1024)
r = getPrime(1024)

modulo = p*r
pseudo_n = r*(pow(e,p,q))
multiplier = getPrime(4)

flag = bytes(FLAG)

print("Pseudo_n = ", pseudo_n)
print("e = ", e)

for i in range(3):
    pt = flag [ i*len(flag)//3 : (i+1)*len(flag)//3 ]
    ct = pow(bytes_to_long(pt),e,(p*q))
    print(f"Ciphertext {i+1} =", ct)


for i in range(5):
    x = input("Enter your lucky number : ")
    try:
        x = int(x)

    except:
        print("Not an integer")
        continue

    if((x<=23)&(x>=3)):
        print("Your lucky output : ", lmao(modulo,multiplier,x))
    else:
        print("Not your lucky day, sad.")
    print("--------------------------------------")

print("Bye!!")