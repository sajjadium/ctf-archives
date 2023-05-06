import json

with open("flag.txt", "rb") as f:
    flag = f.read()

###############################################################
#                                                             #
#  Implemented x-only arithmetic on short Weierstrass curves  #
#                                                             #
###############################################################

class xPoint:
    def __init__(self, X, E):
        k = E.base_field()
        self.X = k(X)
        self.curve = E

    def __repr__(self):
        return f"Point with x-coordinate {self.X} on {E}"

    def __eq__(self, other):
        return self.X == other.X and self.curve == other.curve

def xdbl(P):
    a = P.curve.a4()
    b = P.curve.a6()
    X1 = P.X
    T1 = X1**2
    T4 = T1-a
    T5 = T4**2
    T8 = b*X1
    T9 = 8*T8
    X3 = T5-T9
    T10 = T1+a
    T11 = X1*T10
    T13 = T11+b
    Z3 = 4*T13
    return xPoint(X3/Z3, P.curve)

def xadd(P, Q, R):
    """
    The x-only map (P, Q, P-Q) -> P+Q
    """
    assert R.X != 0
    assert P.curve == Q.curve and Q.curve == R.curve
    a = P.curve.a4()
    b = P.curve.a6()
    X1, X2, X3 = R.X, P.X, Q.X
    if X1:
        # https://hyperelliptic.org/EFD/g1p/auto-code/shortw/xz/diffadd/mdadd-2002-it-3.op3
        # simplified using Z2=Z3=1
        T1 = X2*X3
        T6 = T1-a
        T7 = T6**2
        T9 = 4*b
        T10 = X2+X3
        T11 = T9*T10
        X5 = T7-T11
        T13 = X2-X3
        T14 = T13**2
        Z5 = X1*T14
    else:
        # https://hyperelliptic.org/EFD/g1p/auto-code/shortw/xz/diffadd/mdadd-2002-it-2.op3
        # simplified using Z2=Z3=1
        t2 = X2*X3
        t5 = X2+X3
        t6 = t2+a
        t11 = 4*b
        t12 = t5*t6
        t13 = 2*t12
        R = t13+t11
        t16 = X2-X3
        S = t16**2
        t17 = S*X1
        X5 = R-t17
        Z5 = S
    return xPoint(X5/Z5, P.curve)

def xmult(n, P):
    n = abs(n)
    assert n != 0
    if n == 1:
        return P
    R0, R1, diff = P, xdbl(P), P
    for i in [int(b) for b in bin(n)[3:]]:
        R0pR1 = xadd(R0, R1, diff)
        diff = xadd(R0, R1, R0pR1)
        if i == 0:
            R0, R1 = xdbl(R0), R0pR1
        if i == 1:
            R0, R1 = R0pR1, xdbl(R1)
    return R0

###############################################################
#                                                             #
#                   Challenge begins here                     #
#                                                             #
###############################################################

def gen_pubkeys(G, order):
    s = randint(1,order-1)
    return s, xmult(s, G)

def input_json(prompt: str):
    data = input(prompt)
    try:
        return json.loads(data)
    except:
        print("Please send input as a JSON object")
        exit()

def valid_params(p, A, B):

    if not is_pseudoprime(p):
        print(f"{p} is not prime!!!")
        return False

    if p > 2^270 or p < 2^240:
        print("Please provide a prime between 2^240 and 2^270")
        return False

    F = GF(p)
    E = EllipticCurve(F, [A, B])
    if E.is_singular():
        print("This curve is singular...")
        return False

    if E.is_supersingular():
        print("No MOV-attack!!!")
        return False

    order = E.order()
    cofac = prod([l^e for l,e in list(order.factor(limit=100))[:-1]])

    if E.order() == p or E.order() == p+2:
        print("No trace 1 attack!!!")
        return False

    if not is_pseudoprime(order//cofac) or not order//cofac > 2^240:
        print("Please provide an almost prime-order curve")
        return False

    return True, E, order, cofac



def main():
    print('Send a prime p and curve parameters A, B of the elliptic curve E : y^2 = x^3 + Ax + B')

    p = int(input("p:"))
    A = int(input("A:"))
    B = int(input("B:"))

    valid, E, order, cofac = valid_params(p, A, B)
    if not valid:
        exit()



    F = GF(p)

    E = EllipticCurve(F, [A, B])
    G = xPoint(F(1337), E) # My favorite generator because I am a l33t h4ck3r 8)
    G = xmult(cofac, G)

    print(f"Using generator: {hex(int(G.X))}")

    s1, A = gen_pubkeys(G, order)
    print(f"Alice sends Bob: {hex(int(A.X))}")
    s2, B = gen_pubkeys(G, order)
    print(f"Bob sends Alice: {hex(int(B.X))}")

    shared_secret = xmult(s1, B).X
    assert shared_secret == xmult(s2, A).X

    ss = int(input('What is the shared secret?: '))

    if ss == shared_secret:
        print(f'"flag: {flag}')
    else:
        print({"error": "CDH on prime order curves hard confirmed"})
        exit()

if __name__ == '__main__':
    main()
