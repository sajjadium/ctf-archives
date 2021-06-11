from Crypto.Util.number import getPrime, bytes_to_long, inverse
from secret import flag

assert(len(flag) < 87) # leave space for padding since padding is secure

p = getPrime(1024)
q = getPrime(1024)
n = p*q
e = 3
d = inverse(e,(p-1)*(q-1))
m = bytes_to_long(flag.center(255,"\x00")) # pad on both sides for extra security
c = pow(m,e,n)
print("n = {}".format(n))
print("e = {}".format(e))
print("c = {}".format(c))