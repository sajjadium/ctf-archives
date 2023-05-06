from Crypto.Util.number import *
from secret import flag

m = Integer(int.from_bytes(flag, 'big'))

for _ in range(7):
    p = getPrime(512)
    q = getPrime(512)
    n = p * q
    while 1:
        try:
            a = randint(0,n)
            b = randint(0,n)
            Ep = EllipticCurve(GF(p), [a,b])
            Gp = Ep.lift_x(m) * 2
            Eq = EllipticCurve(GF(q), [a,b])
            Gq = Eq.lift_x(m) * 2
            y = crt([int(Gp[1]),int(Gq[1])],[p,q])
            break
        except Exception as err:
            pass
    print(n, a, b, y)

