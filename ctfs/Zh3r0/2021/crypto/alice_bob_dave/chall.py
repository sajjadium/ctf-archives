from Crypto.Util.number import *
from secret import msg_a,msg_b

e=65537
p,q,r=[getStrongPrime(1024,e) for _ in range(3)]
pt_a=bytes_to_long(msg_a)
pt_b=bytes_to_long(msg_b)

n_a=p*q
n_b=p*r
phin_a=(p-1)*(q-1)
phin_b=(p-1)*(r-1)
d_a=inverse(e,phin_a)
d_b=inverse(e,phin_b)

ct_a=pow(pt_a,e,n_a)
ct_b=pow(pt_b,e,n_b)

print(f"{ct_a=}\n{ct_b=}\n{d_a=}\n{d_b=}\n{e=}")
