import hashlib
from secrets import flag
from Crypto.Util.number import long_to_bytes, bytes_to_long


F = FiniteField(2**256-2**32-2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1)
a = 0
b = 7
E = EllipticCurve(F, [a, b])
G = E((55066263022277343669578718895168534326250603453777594175500187360389116729240,
      32670510020758816978083085130507043184471273380659243275938904335757337482424))
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
Fn = FiniteField(n)

q = floor(1.337*sqrt(n))
K = randint(1, n-1)
low = -1*floor(K/q)
high = floor((n-K)/q)


def hash(msg):
    return Integer('0x' + hashlib.sha256(msg.encode()).hexdigest())


def keygen():
    d = bytes_to_long(flag.encode())
    Q = d * G
    return (Q, d)


def ecdsa_sign(d, m):
    r = 0
    s = 0
    while s == 0:
        k = 1
        while r == 0:
            k = K+randint(low, high)*q
            Q = k * G
            (x1, y1) = Q.xy()
            r = Fn(x1)
        e = hash(m)
        s = Fn(k) ^ (-1) * (e + d * r)
    return [r, s]


def ecdsa_verify(Q, m, r, s):
    e = hash(m)
    w = s ^ (-1)
    u1 = (e * w)
    u2 = (r * w)
    P1 = Integer(u1) * G
    P2 = Integer(u2) * Q
    X = P1 + P2
    (x, y) = X.xy()
    v = Fn(x)
    return v == r


m = ['Hi', 'How are you doing?', 'here are some signatures',
     'for you to understand how this works', 'have fun']
num_sign = len(m)

(Q, d) = keygen()

r = []
s = []

for i in range(num_sign):
    [_r, _s] = ecdsa_sign(d, m[i])
    r.append(_r)
    s.append(_s)

print("r:", r)
print("s:", s)
