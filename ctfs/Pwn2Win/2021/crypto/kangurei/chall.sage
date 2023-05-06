# This code is pretty slow... :(
from Crypto.Util.number import long_to_bytes, bytes_to_long
import numpy as np

FLAG = open("flag.txt", "rb").read()
FLAG = FLAG.ljust((len(FLAG)//24+1)*24, b'\x00')

def mat(G, Xx, n, m):
    h = 0
    X = matrix(G, n, m)
    for i in range(n):
        for j in range(m):
            X[j,i] = Xx[h]
            h+=1
    return X

def vec(G, k):
    return vector(G, k.transpose().list())

def findGama(Gr, t, Tarak, Joao):
    n = 4*t
    D22 = matrix(Gr, n//2, n//2)
    D12 = random_matrix(Gr, n//2, n//2)
    D11 = random_matrix(Gr, n//2, n//2)
    D21 = random_matrix(Gr, n//2, n//2)
    G11 = matrix(Gr, n//2, n//2)

    H = random_matrix(Gr, n, n)
    while not H.is_invertible():
        H = random_matrix(Gr, n, n)
    Hi = H.inverse()

    for i in range(1, n//2):
        for j in range(i):
            D22[i,j] = Gr.random_element()
            G11[i,j] = Gr.random_element()

    bottom = D21.augment(D22)
    Hebert = D11.augment(D12).stack(bottom)
    G = G11.augment(zero_matrix(Gr, n//2, n//2)).stack(bottom)

    RNM = random_matrix(Gr, n, n)

    Cleber = H + (Tarak*(G-Hebert))*Joao
    TAROK = Tarak*(G-Hebert) + ((identity_matrix(Gr, n)-(Tarak*Joao))*RNM)*(identity_matrix(Gr, n) - (Joao*Tarak))

    Gt = G.transpose()
    AMA = identity_matrix(Gr, n)
    AWA = copy(Hi)
    HARDMAT = identity_matrix(Gr, n).tensor_product(Hi)
    for i in range(n):
        AMA = AMA*Gt
        AWA = AWA*Hi
        paw = AMA.tensor_product(AWA)
        HARDMAT = HARDMAT+paw
    return Cleber, Hebert, HARDMAT, TAROK

def inversible_random(G, n, m):
    Upper = identity_matrix(G, n, m)
    Lower = identity_matrix(G, n, m)
    for i in range(1, n):
        for j in range(i-1):
            Lower[i, j] = G.random_element()
            Upper[j, i] = G.random_element()
    A = Lower*Upper
    return A, A.inverse()

def RX(TAROK, Cleber, Bob, Joao, Hebert):
    return ((TAROK*Joao)*TAROK) + (TAROK*Hebert) - (Cleber*TAROK) - Bob

def genkeys(G, t):
    permu = np.random.permutation(int(2*t*t))
    Bob = random_matrix(G, 4*t, 4*t)
    AUX1 = random_matrix(G, 3*t, 4*t)
    C1C1T = AUX1*AUX1.transpose()
    while not C1C1T.is_invertible():
        AUX1 = random_matrix(G, 3*t, 4*t)
        C1C1T = AUX1*AUX1.transpose()
    Joao = AUX1.stack(zero_matrix(G, t, 4*t))
    Karat = AUX1.pseudoinverse()
    Tarak = Karat.augment(zero_matrix(G, 4*t, t))
    Cleber, Hebert, HARDMAT, TAROK = findGama(G, t, Tarak, Joao)
    P1P = random_matrix(G, t, 2*t)
    P2P = random_matrix(G, t, t)
    P3P = random_matrix(G, 2*t, t)
    PP = identity_matrix(G, t).augment(P1P).augment(P2P).stack(zero_matrix(G, 2*t, t).augment(-identity_matrix(G, 2*t)).augment(P3P)).stack(zero_matrix(G, t, 4*t))
    ZERO = Tarak*(((Joao*Tarak)*PP)^2)
    UZAO = random_matrix(G, 4*t, 4*t)
    Lef, Lefter = inversible_random(G, 4*t, 4*t)
    Rig, Righter = inversible_random(G, 4*t, 4*t)
    R = RX(TAROK, Cleber, Bob, Joao, Hebert)
    SecretKey = Joao, Lefter, Rig, R, ZERO, HARDMAT, permu
    LKJ = (Lef*Cleber)*Lefter
    JKL = (Lef*Bob)*Righter
    KLJ = (Rig*Joao)*Lefter
    JLK = (Rig*Hebert)*Righter
    Palona = ((identity_matrix(G, 4*t) - Tarak*Joao)*UZAO)*(identity_matrix(G, 4*t) - Joao*Tarak)
    PRKPL = Righter.transpose().tensor_product(Lef)
    XU = TAROK + Palona
    M = identity_matrix(G, t).augment(zero_matrix(G, t, 2*t)).augment(P1P*P3P + P2P).stack(zero_matrix(G, 2*t, t).augment(-identity_matrix(G, 2*t)).augment(P3P)).stack(zero_matrix(G, t, 4*t))
    Qf = PRKPL*vec(G, Tarak*M+XU)
    MAINMAT = matrix(G, 4096, 0)
    for l in range(2*t*t):
        j = permu[l]
        r = j//(2*t)
        c = j-2*t*r
        M12 = zero_matrix(G, t, 2*t)
        M12[r,c] = 1
        Ml = identity_matrix(G, t).augment(M12).augment(P1P*P3P + P2P - M12*P3P).stack(zero_matrix(G, 2*t, t).augment(-identity_matrix(G, 2*t)).augment(P3P)).stack(zero_matrix(G, t, 4*t))
        ql = (PRKPL*vec(G, Tarak*Ml+XU))-Qf
        MAINMAT = MAINMAT.augment(ql)
    MAINMAT = MAINMAT.augment(Qf)
    MAINMAT = MAINMAT.augment(zero_matrix(G, 4096, 7))
    PublicKey = LKJ, JKL, KLJ, JLK, MAINMAT
    return SecretKey, PublicKey

def encrypt(G, PublicKey, message, t):
    Cleber, Bob, Joao, Hebert, MAINMAT = PublicKey
    msg = []
    for x in message:
        for k in range(8):
            msg.append((x>>(7-k))&1)
    for _ in range(192, 2*t*t):
        msg.append(G.random_element())
    msg.append(1)
    for _ in range(7):
        msg.append(0)
    X = mat(G, MAINMAT*vector(G, msg), 4*t, 4*t)
    Yt = RX(X, Cleber, Bob, Joao, Hebert)
    return long_to_bytes(int("".join([str(k) for k in Yt.list()]), 2))

def decrypt(G, SecretKey, enc, t):
    Yt = matrix(G, 4*t, 4*t)
    k = 0
    for i in range(Yt.dimensions()[0]):
        for j in range(0, Yt.dimensions()[1], 8):
            for l in range(8):
                Yt[i, j+l] = (enc[k]>>(7-l))&1
            k+=1
    Joao, Lefter, Rig, R, ZERO, HARDMAT, permu = SecretKey
    WHY = (Lefter*Yt)*Rig
    OPOP = WHY - R - ZERO
    POPO = mat(G, HARDMAT*vec(G, OPOP), 4*t, 4*t)
    M = Joao*POPO
    M12 = matrix(G, t, 2*t)
    for i in range(t):
        for j in range(2*t):
            M12[i, j] = M[i, t+j]
    msg = []
    for l in range(192):
        j = permu[l]
        r = j//(2*t)
        c = j-2*t*r
        msg.append(str(M12[r, c]))
    return long_to_bytes(int("".join(msg), 2))

G = GF(2)
t = 16

SecretKey, PublicKey = genkeys(G, t)
Joao, Lefter, Rig, R, ZERO, HARDMAT, permu = SecretKey
LKJ, JKL, KLJ, JLK, MAINMAT = PublicKey

open("PkeyA", "w").write(LKJ.str())
open("PkeyB", "w").write(JKL.str())
open("PkeyC", "w").write(KLJ.str())
open("PkeyD", "w").write(JLK.str())
open("PkeyQ", "w").write(MAINMAT.str())

enc1 = encrypt(G, PublicKey, FLAG[:24], t)
open('ct', 'wb').write(enc1)
enc2 = encrypt(G, PublicKey, FLAG[24:24*2], t)
open('ct2', 'wb').write(enc2)
enc3 = encrypt(G, PublicKey, FLAG[24*2:], t)
open('ct3', 'wb').write(enc3)
