import Crypto.Util.number as nt
from binascii import *

#cybears 2020 params
p = 273540544991637969479760315194669352313
a = int(hexlify(b'cybears'), 16)
b = 2020

gx = 27880441596758306727342197655611673569
gy = 214924393757041059014541565759775133463

order = 273540544991637969474690923574060066154

class ec_point:
    def __init__(self,E, x,y):
        self.x = x % E.p
        self.y = y % E.p

class ec_curve:
    def __init__(self, p, a, b):
        self.p = p
        self.a = a
        self.b = b

E = ec_curve(p,a,b)
G = ec_point(E, gx,gy)

O = ec_point(E, 0,1) #Point at Infinity

def ec_inverse(E, P):
    return ec_point(E, P.x, (-P.y) % E.p)

def ec_isInf(P):
    if P.x == 0 and P.y == 1:
        return True
    else:
        return False

def ec_equals(P1,P2):
    if P1.x == P2.x and P1.y == P2.y:
        return True
    else:
        return False

def ec_add(E, P1,P2):
    if ec_isInf(P1):
        return P2
    if ec_isInf(P2):
        return P1
    if ec_equals(P1, ec_inverse(E, P2)):
        return O

    if ec_equals(P1,P2):
        m = (3*P1.x**2 + E.a) * nt.inverse(2*P1.y,E.p)
    else:
        m = (P2.y - P1.y)*nt.inverse((P2.x-P1.x) , E.p)

    x3 = m*m - P1.x - P2.x
    y3 = m*(P1.x - x3) - P1.y

    return ec_point(E,x3,y3)

def ec_scalar(E,k,P):
    result = O
    Q = ec_point(E, P.x, P.y)
    while (k > 0):
        if k%2 == 1: #isodd(k)
            result = ec_add(E,result, Q)
        Q = ec_add(E,Q,Q)
        k = k >> 1
    return result
