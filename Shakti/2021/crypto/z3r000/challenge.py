from Crypto.Util.number import *
from secret import flag

p = getPrime(1024)
q = getPrime(1024)
n = p*q
e = 3

flag = flag + "\x00"*200
ct = pow(bytes_to_long(flag),e,n)

print(n)
print(ct)






