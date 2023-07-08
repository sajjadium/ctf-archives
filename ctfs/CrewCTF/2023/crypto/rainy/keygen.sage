load("/home/sage/common.sage")


def generate_affine(size):
    while True:
        M = Matrix(K, size, size, [K.random_element() for _ in range(size**2)])
        if M.determinant() != 0:
            break
    v = vector(K, size, [K.random_element() for _ in range(size)])
    return (M, v)


def generate_layer1():
    polys = []
    for _ in range(o1):
        poly = {}
        for i in range(v1):
            for j in range(i, v2):
                poly[i, j] = K.random_element()
        polys.append(poly)
    return polys


def generate_layer2():
    polys = []
    for _ in range(o2):
        poly = {}
        for i in range(v2):
            for j in range(i, v3):
                poly[i, j] = K.random_element()
        polys.append(poly)
    return polys


def genkey():
    (A, a) = generate_affine(n)
    (B, b) = generate_affine(m)
    centralmap = generate_layer1() + generate_layer2()
    Ax = vecadd(matmul(A, yi), a)
    F_Ax = []
    for centralmapele in centralmap:
        F_Ax_ele = 0
        for (i, j), Kele in centralmapele.items():
            F_Ax_ele += Kele * Ax[i] * Ax[j]
        F_Ax.append(F_Ax_ele)
    B_F_Ax = vecadd(matmul(B, F_Ax), b)
    return B_F_Ax, ((A, a), centralmap, (B, b))


for i in range(20):
    pubkey, privkey = genkey()
    
    Ktostr = lambda x:''.join(map(str, x.polynomial().list())).ljust(4, '0')
    
    fpriv = open(f'/home/sage/privkey_{i}', 'w')
    fpriv.write(f'privkey_0=({list(map(Ktostr, privkey[0][0].list()))}, {list(map(Ktostr, privkey[0][1].list()))})'+'\n')
    fpriv.write(f'privkey_1={[{(i,j):Ktostr(privkey[1][k][(i,j)]) for (i, j) in privkey[1][k].keys()} for k in range(m)]}'+'\n')
    fpriv.write(f'privkey_2=({list(map(Ktostr, privkey[2][0].list()))}, {list(map(Ktostr, privkey[2][1].list()))})')
    fpriv.close()
    
    fpub = open(f'/home/sage/pubkey_{i}', 'w')
    fpub.write(f'pubkey={[{e:Ktostr(c) for e,c in zip(pubkey[i].exponents(), pubkey[i].coefficients())} for i in range(m)]}')
    fpub.close()
