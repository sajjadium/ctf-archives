K.<X> = GF(2**4, name='X')


v1 = 20
v2 = 30
v3 = n = 46
o1 = v2 - v1 # 10
o2 = v3 - v2 # 16
m = n - v1 # 26
P = PolynomialRing(K, n, [f"y{i}" for i in range(n)])
yi = P.gens()


Ktostr = lambda x:''.join(map(str, x.polynomial().list())).ljust(4, '0')
strtoK = lambda x: sum([int(x[i])*X**i for i in range(4)])


def encodeK(msg, size):
    msglong = int.from_bytes(msg, byteorder='big')
    if msglong.bit_length() > size * 4:
        raise ValueError
    msgbin = bin(msglong)[2:].zfill(size * 4)
    return [strtoK(msgbin[j:j+4]) for j in range(0, len(msgbin), 4)]


def decodeK(sigK, size):
    if len(sigK) != size:
        raise ValueError
    siglong = int(''.join([Ktostr(sigKele) for sigKele in sigK]), 2)
    return siglong.to_bytes((4*size)//8, byteorder='big')


def matmul(Mat, Vec):
    if Mat.ncols() != len(Vec):
        raise ValueError
    return [sum([Mat[i][j] * Vec[j] for j in range(len(Vec))]) for i in range(Mat.nrows())]


def vecadd(Vec1, Vec2):
    if len(Vec1) != len(Vec2):
        raise ValueError
    return [Vec1[i] + Vec2[i] for i in range(len(Vec1))]


def vecneg(Vec):
    return [-Vec[i] for i in range(len(Vec))]
