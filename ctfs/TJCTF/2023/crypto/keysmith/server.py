#!/usr/local/bin/python3.10 -u
from Crypto.Util.number import getPrime
flag = open("flag.txt", "r").read()

po = getPrime(512)
qo = getPrime(512)
no = po * qo
eo = 65537

msg = 762408622718930247757588326597223097891551978575999925580833
s = pow(msg,eo,no)

print(msg,"\n",s)

try:
    p = int(input("P:"))
    q = int(input("Q:"))
    e = int(input("E:"))
except:
    print("Sorry! That's incorrect!")
    exit(0)

n = p * q
d = pow(e, -1, (p-1)*(q-1))
enc = pow(msg, e, n)
dec = pow(s, d, n)
if enc == s and dec == msg:
    print(flag)
else:
    print("Not my keys :(")
