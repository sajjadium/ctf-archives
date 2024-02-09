import math
from Crypto.Util.number import *
from secret import flag,p,q
from gmpy2 import next_prime
m = bytes_to_long(flag.encode())
n=p*q


power1=getPrime(128)
power2=getPrime(128)
out1=pow((p+5*q),power1,n)
out2=pow((2*p-3*q),power2,n)
eq1 = next_prime(out1)

c = pow(m,eq1,n)


with open('chall2.txt', 'w') as f:
    f.write(f"power1={power1}\npower2={power2}\neq1={eq1}\nout2={out2}\nc={c}\nn={n}")



