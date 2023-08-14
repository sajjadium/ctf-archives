import random
import Crypto.Util.number as number
import numpy as np
import json
import sys
import galois

p = number.getPrime(2050)

f = galois.GF(p,verify=False,primitive_element=2)

k=8
num = 12

secret = sys.argv[1]

a = [random.randint(0,f.order) for _ in range(k-1)]
a.append(secret)
a = f(a)

def poly(a,x):
    return np.sum([ a[i]*(x**(len(a)-i-1)) for i in range(len(a))])

i_s = [random.randint(0,f.order) for i in range(1,num+1,1)]
shared_secrets = [(i,poly(a,f(i))) for i in i_s]

print ('\n'.join( [ '{"i":%d,"value":%d}' %(s[0],int(s[1])) for s in shared_secrets ]))
