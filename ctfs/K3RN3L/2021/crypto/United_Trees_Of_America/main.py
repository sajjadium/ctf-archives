import random
import math
from Crypto.Util.number import *
def isPrime(p):
    for i in range(2,int(math.sqrt(p))+1):
        if p%i==0: return False
    return True
flag = bytes_to_long(open('flag.txt','rb').read())
p = int(input('Enter a prime: '))
assert 10<p, 'Prime too small'
assert p<250, 'Prime too big'
assert isPrime(p), 'Number not prime'
coeffs = [random.getrandbits(128) for _ in range(1000)]
k = sum([coeffs[i] for i in range(0,len(coeffs),p-1)])
coeffs[0] += flag - k
def poly(coeffs,n,p):
    return sum([c*pow(n,i,p) for i,c in enumerate(coeffs)])%p
n = int(input('Enter a number: '))
assert 1<n<p-1, 'We\'re feeling sneaky today, hmm?'
op = 0
for i in range(1,p):
    op += poly(coeffs,pow(n,i,p),p)
print(op%p)
