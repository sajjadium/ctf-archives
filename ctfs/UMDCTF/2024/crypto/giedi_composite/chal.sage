import random
from Crypto.Util.number import bytes_to_long, long_to_bytes

N = 210
q = 2003 # this one can be prime instead :)
p = 3


def encode_msg(msg):
    m = bin(bytes_to_long(msg))[2:].zfill(N)
    return [0 if c == '0' else 1 for c in m]


def decode_msg(m):
    n = 0
    for b in m:
        n *= 2
        n += b
    return long_to_bytes(n)

Fq = Zmod(q)
Fp = Zmod(p)
Rq = PolynomialRing(Fq, 'x').quotient(x^N - 1)
Rp = PolynomialRing(Fp, 'x').quotient(x^N - 1)
Rx.<x> = PolynomialRing(ZZ, 'x')
Qx = PolynomialRing(QQ, 'x')

while True:
    f = Rx([random.choice([-1,0,1]) for _ in range(N)])
    if gcd(f, x^N - 1) == 1:
        if Rp(f).is_unit():
            f_p = Rp(f).inverse()
        else:
            continue
        if Rq(f).is_unit():
            f_q = Rq(f).inverse()
        break

g = Rx([random.choice([-1,0,1]) for _ in range(N)])

priv = (f, f_p)

pub = p * f_q * Rq(g)


print("Public key:")
print(pub.list())


flag = open('flag.txt', 'rb').read()

msg = Rx(encode_msg(flag))

b = Rx([random.choice([-2,-1,0,1,2]) for _ in range(N)])

ct = (b * pub + Rq(msg))

print("Ct: ")
print(ct.list())

