from Crypto.Util.number import *
from collections import namedtuple


# define complex number
Complex=namedtuple("Complex", "r c")

# define complex multiplication
def Complex_Mul(P, Q):
    R=P.r*Q.r-P.c*Q.c
    C=P.r*Q.c+Q.r*P.c
    return Complex(R, C)

# define how to turn message into complex number
def Int_to_Complex(x):
    R=0
    C=0
    cnt=0
    while(x>0):
        if(cnt%2==0):
            R+=(x%2)<<cnt
        else:
            C+=(x%2)<<cnt
        x>>=1
        cnt+=1
    return Complex(R, C)

# keys
p, q=???, ???
P=Complex(p, 2*q)
Q=Complex(q, 2*p)
N=Complex_Mul(P, Q)

# generate flag
flag=b'THJCC{FAKE_FLAG}'
m=bytes_to_long(flag)
M=Int_to_Complex(m)
e=65537
C=Complex(pow(M.r, e, N.r*-1), pow(M.c, e, N.c)) # N.r*-1 is because I don't want to define modular under negative number

print(f'{N=}')
print(f'{e=}, {C=}')