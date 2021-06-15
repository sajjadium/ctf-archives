import time
from Crypto.Util.number import *
flag = open('flag.txt','r').read()
p = getPrime(1024)
q = getPrime(1024)
e = 2**16+1
n=p*q
ct=[]
for ch in flag:
    ct.append((ord(ch)^e)%n)
print(n)
print(e)
print(ct)
