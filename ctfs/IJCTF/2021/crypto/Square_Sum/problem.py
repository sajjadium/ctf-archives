from Crypto.Util.number import getPrime, inverse, bytes_to_long
from Crypto.Random.random import randint
from secret import MSG, FLAG


p = getPrime(1024)
q = getPrime(1024)
n = p * q

n2 = n**2
halfpq_sqr_sum = (p//2)**2 + (q//2)**2

k = randint(1, n-1)
g = 1 + k*n
r = randint(2, n2-1)

cmsg = (pow(g, bytes_to_long(MSG), n2) * pow(r, n2, n2)) % n2
c = (bytes_to_long(FLAG) * pow(r, n, n2)) % n2

print('n2='+str(n2))
print('halfpq_sqr_sum='+str(halfpq_sqr_sum))
print('cmsg='+str(cmsg))
print('c='+str(c))
