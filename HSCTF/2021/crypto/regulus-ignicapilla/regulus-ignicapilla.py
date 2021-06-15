from Crypto.Util.number import *
import random
import math
flag = open('flag.txt','rb').read()
while 1:
    p = getPrime(512)
    q = getPrime(512)
    if (p<q or p>2*q):
        continue
    break
n = p**2*q
while 1:
    a = random.randint(2,n-1)
    if pow(a,p-1,p**2)!=1:
        break
def e(m):
    assert m<p
    kappa = random.randint(1,n-1)
    return (pow(a,m,n)*pow(pow(a,n,n),kappa,n))%n
sigma = random.randint(2,q-1)
tau = (p**2*sigma-random.randint(1,2**1340))//q**2+random.randint(1,2**335)
rho = p**2*sigma+q**2*tau+random.randint(1,2**1160)
c = e(bytes_to_long(flag))
print(n,a,c)
print(sigma,tau,rho)
