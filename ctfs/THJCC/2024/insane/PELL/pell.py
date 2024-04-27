from Crypto.Util.number import *
from Crypto.Cipher import AES
from collections import namedtuple
import os

# define some stuffs about point
Point=namedtuple("Point", "x y")
def Point_Addition(P, Q):
    X=(P.x*Q.x+d*P.y*Q.y)%p
    Y=(Q.x*P.y+P.x*Q.y)%p
    return Point(X, Y)


def Point_Power(P, x):
    Q=Point(1, 0)
    while(x>0):
        if x%2==1:
            Q=Point_Addition(Q, P)
        x>>=1
        P=Point_Addition(P, P)
    return Q


# encryption
key=os.urandom(16)
m=bytes_to_long(key)
cipher = AES.new(key, AES.MODE_ECB)
flag=b'THJCC{FAKE_FLAG}'
p=22954440473064692367638020521915192869513867655951252438024058919141
d=1008016
G=Point(1997945712322124204937815965902875623145811005630602636960422269513, 252985428778294107560116770944951015145970075431259613311231816)
C=Point_Power(G, m)
print(f"{C=}\n{p=}\n{d=}")
secret=bytes_to_long(cipher.encrypt(flag))
print(f"{secret=}") 