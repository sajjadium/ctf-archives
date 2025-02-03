from Crypto.Util.number import getPrime, bytes_to_long
from Crypto.Util.Padding import pad

with open('flag.txt','rb') as fil:
    FLAG = fil.read()

e = 2
p = getPrime(512)
q = getPrime(512)
n = p*q

print(f'{e = }')
print(f'{p = }')
print(f'{q = }')
print(f'{n = }')

m = bytes_to_long(pad(FLAG,100))
c = pow(m, e, n)

print(f'{c = }')

phi = (p-1)*(q-1)
d = pow(e,-1,phi) # It always errors here?!!?!

print(f'{phi = }')
print(f'{d = }')

pt = pow(c,d,n)
assert pt == m
