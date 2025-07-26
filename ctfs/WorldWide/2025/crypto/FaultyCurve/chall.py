def add(P, Q, a, p):
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 != y2 or y1 == 0):
        return None
    if x1 == x2:
        m = (3 * x1 * x1 + a) * pow(2 * y1, -1, p) % p
    else:
        m = (y2 - y1) * pow(x2 - x1, -1, p) % p
    x3 = (m * m - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    return (x3, y3)

def mul(k, P, a, p):
    R0 = None
    R1 = P
    for bit in bin(k)[2:]:
        if bit == '0':
            R1 = add(R0, R1, a, p)
            R0 = add(R0, R0, a, p)
        else:
            R0 = add(R0, R1, a, p)
            R1 = add(R1, R1, a, p)
    return R0


flag = int.from_bytes(b"wwf{???????????????????????????}")

from secret import p, a, b, G
# EllipticCurve(GF(p), [a,b]) in sage gives an error for some reason :sob: 
# Some error in /src/sage/schemes/elliptic_curves but i'm too nub to figure out why :sob: :sob:
Gx = G[0]
Qx = mul(flag, G, a, p)[0]
print(f'{p = }')
print(f'{a = }')
print(f'{Gx = }')
print(f'{Qx = }')
"""
p = 3059506932006842768669313045979965122802573567548630439761719809964279577239571933
a = 2448848303492708630919982332575904911263442803797664768836842024937962142592572096
Gx = 3
Qx = 1461547606525901279892022258912247705593987307619875233742411837094451720970084133
"""