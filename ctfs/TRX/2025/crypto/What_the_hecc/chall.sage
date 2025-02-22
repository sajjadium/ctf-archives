set_verbose(-1)

Zp = Zmod(2**127 - 1)
R.<x> = PolynomialRing(Zp)

a, b = 57792482556163740063210341500068239889, 169237172037427005576500528337261655640
F = x**5 + a*x**3 + b*x
H = x**2 + x + 1

def random_jp():
    global x
    while True:
        Px = Zp.random_element()
        rts = (x**2 + H(Px)*x - F(Px)).roots()
        if rts:
            return x - Px, choice(rts)[0]

def add(ua, va, ub, vb):

    t, c, d = ub.xgcd(va + vb + H)
    g, a, b = ua.xgcd(t)

    s1, s2, s3, d = a, b*c, b*d, g

    u = (ua * ub) // (d**2)
    v = (s1 * ua * vb + s2 * ub * va + s3 * (va * vb + F)) * d.inverse_mod(u)
    v = v.mod(u)

    while u.degree() > 2:
        u = ((v**2 + v*H - F) // u).monic()
        v = (-v -H).mod(u)
    
    return u, v

P, Q, R, S = [random_jp() for _ in range(4)]

print("P+Q+R =", add(*P,*add(*Q, *R))[0])
print("P+Q+S =", add(*P,*add(*Q, *S))[0])

import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
FLAG = "TRX{***}"

secret = hashlib.sha256(''.join(map(str, [P, Q, R, S])).encode()).digest()
cipher = AES.new(key=secret, mode=AES.MODE_CBC)
iv = cipher.iv
ct = cipher.encrypt(pad(FLAG.encode(), AES.block_size))

print(f"{iv.hex() = }")
print(f"{ct.hex() = }")