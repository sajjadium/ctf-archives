import sys,os
class X(object):
    def __init__(x,a=0,b=0,c=0):
        x.a=a
        x.b=b or ~-a
        x.c=c
    def __invert__(x):
        x.c-=x.c
        return X(x.a,x.b,x.c)
    def __pow__(x, y):
        x=~x
        x.a*=y
        x.b*=y
        x.c+=3
        return x
    def __pos__(x):
        x**=3
        x.b=-~x.b
        return x
    def __neg__(x):
        x**=3
        return x
    def __or__(x, y):
        y**=(~x).a
        y.b+=x.b
        return y
    def __add__(x, y):
        return x|+y
    def __sub__(x, y):
        return x|-y
    def __del__(x):
        if not x.c: return
        y=[0]*9
        while 3**y[8]<x.a:
            z=x.b//3**y[8]%3**7
            y[8]+=7
            a=z//3**4
            b=z//9%9
            c=z%9
            d=c+x.b//3**y[8]%3**7*3*3
            if   a==0:
                os._exit(0)
            elif a==1:
                y[8]+=7
                y[b]=d
            elif a==2:
                y[b]=y[c]
            elif a in(3,8):
                y[b]=x.b//3**y[c]%3**(3*3)
                if a==8:
                    y[c]+=9
                    y[c]%=3**9
            elif a in(4,6,7):
                if a==6:
                    y[8]+=7
                    b,c,d=8,7,d or y[b]
                if a>4:
                    y[c]-=9
                    y[c]%=3**9
                x.b+=y[b]*3**y[c]-x.b//3**y[c]%3**9*3**y[c]
                if a==6:
                    y[8]=d
            elif a==5:
                if y[b]:
                    y[8]=d
                else:
                    y[8]+=7
                pass
            elif 9<=a<=12:
                y[b]={
                     9:lambda a,b:a<b,
                    10:lambda a,b:(a+b)%3**9,
                    11:lambda a,b:(a*b)%3**9,
                    12:lambda a,b:(a-b)%3**9,
                }[a](y[b],y[c])
            elif 13<=a<=15:
                e,f=0,y[c]
                for _ in range(9):
                    e*=3
                    e+={
                        13:lambda a,b:~(a+b)%3,
                        14:lambda a,b:min(a,b),
                        15:lambda a,b:max(a,b),
                    }[a](y[b]%3,f%3)
                    y[b]//=3
                    f//=3
                for _ in range(9):
                    y[b]*=3
                    y[b]+=e%3
                    e//=3
            elif a==16:
                y[b]=y[b]*3**c%3**9
            elif a==17:
                y[b]=y[b]//3**c
            elif a==18:
                y[b]=ord(sys.stdin.read(1))
            elif a==19:
                sys.stdout.write(chr(y[b]));sys.stdout.flush()
            else:
                0/0
for i in range(1, 100):
    setattr(sys.modules['__main__'],'_'*i,X(3**i))
