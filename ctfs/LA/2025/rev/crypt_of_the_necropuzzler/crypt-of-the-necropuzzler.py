#!/usr/local/bin/python3
import tty
import sys
import hashlib

if sys.stdin.isatty():
    tty.setcbreak(0)

g=(f:=[0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1])[:]
n=[1,1,0,0,0,0,0,0,1,0,2,0,0,0,0,0,3,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,3,0,0,0,1,0,1,0,1,0,0,0,2,2,2,0,0]

def decrypt_flag(k):
    h=hashlib.sha512(str(k).encode()).digest()
    print(bytes(a^b for(a,b)in zip(h,bytes.fromhex("8b1e35ac3da64cb9db365e529ad8c9496388a4f499faf887386b4f6c43b616aae990f17c1b1f34af514800275673e0f3c689c0998fc73c342f033aa7cc69d199"))).decode())

m={'w':(-1,0),'s':(1,0),'a':(0,-1),'d':(0,1)}
def t(a,b,s=None):
    if s is None:
        s = set()
    s.add((a,b))
    for(i,j)in m.values():
        x,y=a+i,b+j
        if (x,y) not in s and x in range(7) and y in range(7) and g[x*7+y]==g[a*7+b]:
            t(x,y,s)
    return s

a,b=0,0
d=1
while 1:
    if d:
        print("\x1b[2J")
        for i in range(7):
            print(" ["[(a,b)==(i,0)],end="")
            for j in range(7):
                print("_#"[g[i*7+j]],end="["if(a,b)==(i,j+1)else" ]"[(a,b)==(i,j)])
            print()
        d=0
    try:
        c=sys.stdin.read(1)
        if c == "":
            break
    except EOFError:
        break
    if c=='q':
        break
    elif c=='x':
        if not f[i:=a*7+b]:
            g[i]=1-g[i]
            d=1
    elif v:=m.get(c):
        i,j=a+v[0],b+v[1]
        if i in range(7) and j in range(7):
            a,b=i,j
            d=1
    elif c=='c':
        p=1
        s=set()
        for i in range(7):
            for j in range(7):
                if(i,j)not in s:
                    v=[0]*4
                    k=t(i,j)
                    s|=k
                    for(x,y)in k:
                        v[n[x*7+y]]+=1
                    if any(h not in (0,2) for h in v[1:]):
                        p=0
        if p:
            print("Correct!")
            decrypt_flag(g)
        else:
            print("Incorrect!")


