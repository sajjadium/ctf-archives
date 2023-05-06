#! /usr/bin/sage
from sage.all import *
from Crypto.Util.number import *
from util import Complex
from secrets import flag

def PowPlus(msg,k):
    c=Complex(msg[0],msg[1])
    while k>0:
        if k%2:
            k-=1
            c.OnePlus()
        else:
            k//=2
            c.Double()
    return c.val(),c.Christmas_gift()

def gen():
    a,b,x = seed
    while 1:
        x = (a*x + b) % p
        yield x
def Function_function(x):
    f=0
    g = gen()
    for e in range(6):
        f+= next(g)*(x^e)
    return f



p = random_prime(1<<512)
seed = [randint(2, p-1) for _ in range(3)]
vs = [(i, Function_function(i)) for i in range(1, 5)]
print(f"p={p}")
print("fvs={vs}")


flag = Function_function(bytes_to_long(flag))
assert len(bin(flag)) == 1586
FBytes = long_to_bytes(flag)
m1 = bytes_to_long( FBytes[:len(FBytes)//2])
m2 = bytes_to_long( FBytes[len(FBytes)//2:])
msg = (m1,m2)
k=0x10001
val,gift = PowPlus(msg,k)

print(f'val={val}')
print(f'gift={gift}')


