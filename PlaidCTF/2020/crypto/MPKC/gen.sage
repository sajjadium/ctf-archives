# Jiahui Chen et al. cryptosystem, 80-bit security
# WARNING: very slow implementation.
import sys
q,n,a,s = (3,59,10,25)
m = n+1-a+s
FF = GF(q)
R = PolynomialRing(FF, ["x{}".format(i) for i in range(n)])
xs = R.gens()

def keygen():
    while True:
        C = random_matrix(FF, n+1, n)
        if matrix(FF, [2*C[i]-2*C[i+1] for i in range(n)]).is_invertible():
            break

    FC = []
    for i in range(n+1):
        p = 0
        for j in range(n):
            p += (xs[j] - C[i][j])^2
        FC.append(p)

    while True:
        S_lin = random_matrix(FF, n, n)
        if S_lin.is_invertible():
            break
    S_trans = (FF^n).random_element()
    S = (S_lin, S_trans)

    while True:
        T_lin = random_matrix(FF, m, m)
        if T_lin.is_invertible():
            break
    T_trans = (FF^m).random_element()
    T = (T_lin, T_trans)

    G = []
    for i in range(s):
        G.append(R.random_element(degree=2, terms=Infinity))
    F = FC[:n+1-a] + G

    P = vector(xs)
    P = S[0]*P
    P += S[1]
    v = []
    for i in range(len(F)):
        v.append(F[i](*P))
        print("keygen {}/{}".format(i+1,len(F)), file=sys.stderr)
    P = vector(v)
    P = T[0]*P
    P += T[1]
    print("done keygen", file=sys.stderr)

    return (P, (C, G, S, T))

def make_blocks(ss):
    x = 0
    for i in ss:
        x = x*256+ord(i)
    v = []
    while x > 0:
        v.append(FF(x%q))
        x = x//q
    v += [FF(0) for i in range(n - (len(v) % n))]
    blocks = []
    for i in range(0, len(v), n):
        blocks.append(vector(v[i:i+n]))
    return blocks

def combine_blocks(blocks):
    x = 0
    for i in blocks[::-1]:
        for j in i[::-1]:
            x = x*q+Integer(j)
    ss = ""
    while x > 0:
        ss = chr(x % 256) + ss
        x = x//256
    return ss

def encrypt_block(plain, pk):
    return pk(*plain)

def encrypt(plain, pk):
    blocks = make_blocks(plain)
    enc = []
    for i in range(len(blocks)):
        print("encrypt {}/{}".format(i+1,len(blocks)), file=sys.stderr)
        enc.append(encrypt_block(blocks[i], pk))
    return enc

def decrypt_block(cipher, sk):
    C, G, S, T = sk
    C2I = matrix(FF, [2*C[i]-2*C[i+1] for i in range(n)]).inverse()
    cv = []
    for i in range(n):
        cc = 0
        for j in range(n):
            cc += C[i+1][j]^2 - C[i][j]^2
        cv.append(cc)
    cv = vector(cv)
    g1 = T[0].inverse()*(cipher - T[1])
    for g2 in FF^a:
        print("decrypt: trying:", g2, file=sys.stderr)
        g = vector(list(g1)[:n+1-a]+list(g2))
        g_diff = vector([g[i+1]-g[i] for i in range(len(g)-1)])
        d = C2I * (g_diff-cv)
        for i,j in zip(G,g1[n+1-a:]):
            if i(*d) != j:
                break
        else:
            return S[0].inverse() * (d - S[1])

def decrypt(cipher, sk):
    dec = []
    for i in range(len(cipher)):
        print("decrypt {}/{}".format(i+1,len(cipher)), file=sys.stderr)
        dec.append(decrypt_block(cipher[i], sk))
    return combine_blocks(dec)

pk, sk = keygen()
print(pk)
flag = open("flag.txt").read().strip()
print(encrypt(flag, pk))
