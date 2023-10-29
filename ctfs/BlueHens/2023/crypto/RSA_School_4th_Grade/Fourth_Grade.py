from Crypto.Util.number import *
e=65537
your_e = getPrime(20)
msg=bytes_to_long(b'UDCTF{REDACTED}')
p=getPrime(512)
q=getPrime(512)
n=p*q
assert(msg < n)
ct=pow(msg, e, n)
your_d = inverse(your_e, (p-1)*(q-1))
print(your_e)
print(your_d)
print(n)
print(e)
print(ct)
