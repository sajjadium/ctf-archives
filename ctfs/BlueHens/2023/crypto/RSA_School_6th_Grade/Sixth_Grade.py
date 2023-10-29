from Crypto.Util.number import *
msg=b'UDCTF{REDACTED}'
pt=bytes_to_long(msg)
p1=getPrime(512)
q1=getPrime(512)
N1=p1*q1
e=3
ct1=pow(pt,e,N1)
p2=getPrime(512)
q2=getPrime(512)
N2=p2*q2
ct2=pow(pt,e,N2)
p3=getPrime(512)
q3=getPrime(512)
N3=p3*q3
ct3=pow(pt,e,N3)

print(N1)
print(N2)
print(N3)
print(e)
print(ct1)
print(ct2)
print(ct3)
