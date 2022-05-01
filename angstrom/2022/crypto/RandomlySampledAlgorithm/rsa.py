from Crypto.Util.number import getStrongPrime
f = [REDACTED]
m = int.from_bytes(f,'big')
p = getStrongPrime(512)
q = getStrongPrime(512)
n = p*q
e = 65537
c = pow(m,e,n)
print("n =",n)
print("e =",e)
print("c =",c)
print("phi =",(p-1)*(q-1))
