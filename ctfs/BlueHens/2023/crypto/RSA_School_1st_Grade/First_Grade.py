from Crypto.Util.number import *
p=getPrime(512)
q=getPrime(512)
n=p*q
e=65537
msg=bytes_to_long(b'UDCTF{REDACTED}')
ct=pow(msg,e,n)
print(p)
print(n)
print(e)
print(ct)
