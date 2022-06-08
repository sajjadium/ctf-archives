from Crypto.Util.number import *
import random
import itertools
flag = open('flag.txt','rb').read()
pt = bytes_to_long(flag)
p,q = getPrime(512),getPrime(512)
n = p*q
a = random.randint(0,2**512)
b = random.randint(0,a)
c = random.randint(0,b)
d = random.randint(0,c)
e = random.randint(0,d)
f = 0x10001
g = [[-a,0,a],[-b,0,b],[-c,0,c],[-d,0,d],[-e,0,e]]
h = list(pow(sum(_),p,n) for _ in itertools.product(*g))
random.shuffle(h)
print(h[0:len(h)//2])
print(n)
print(pow(pt,f,n))