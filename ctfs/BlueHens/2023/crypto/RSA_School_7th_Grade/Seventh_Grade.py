from Crypto.Util.number import *
import sympy.ntheory as nt
import random
p=getPrime(1024)
q=nt.nextprime(p)
for _ in range(random.randint(500,10000)):
    q=nt.nextprime(q)
N=p*q
msg="UDCTF{REDACTED}"
pt=bytes_to_long(msg)
e=65537
ct=pow(pt,e,N)
print(N)
print(e)
print(ct)
