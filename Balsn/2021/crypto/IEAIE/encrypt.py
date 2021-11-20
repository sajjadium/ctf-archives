#!/usr/bin/env python3
from lib import *
from subprocess import *
import numpy as np
import sys
import concurrent.futures
import base64
from scipy.stats import entropy

def Encrypt(A):
    # Step 1
    (m, n) = A.shape
    s = Entropy(A)

    x_0, y_0 = UpdateKey1(x0, y0, xp0, yp0, s)
    P_seq = LASM2D(mu, x_0, y_0, m*n)
    P = P_seq.reshape(A.shape)

    # Step 2
    a = np.ceil((x0+y0+1)*(10**7)) % (m)
    b = np.ceil((xp0+yp0+2)*(10**7)) % (n)
    u = P[int(a), :]
    v = P[:, int(b)]
    up = np.ceil(u*(10**14)) % (n)
    vp = np.ceil(v*(10**14)) % (m)
    up = up.astype(int)
    vp = vp.astype(int)
    Uniq(up)
    Uniq(vp)
    B = np.zeros(A.shape, dtype='uint8')
    tmp = np.zeros(A.shape, dtype='uint8')
    for i in range(n):
        tmp[:, up[i]] = A[:, i]
    for i in range(m):
        B[vp[i], :] = tmp[i, :]
    
    # Step 3
    W = np.zeros(A.shape, dtype='uint8')
    for i in range(m):
        for j in range(n):
            W[i][j] = (m*n+(i+1)+(j+1)) % 256
    R = (B+W) % 256

    # Step 4
    xp_0, yp_0 = UpdateKey2(x0, y0, xp0, yp0)
    K_seq = LASM2D(mu, xp_0, yp_0, m*n)
    K = K_seq.reshape(A.shape)
    K = np.ceil(K*(10**14)) % 256
    K = K.astype('uint8')

    # Step 5
    C = np.zeros(A.shape, dtype='uint8')

    column_count = np.zeros((n-1, 256), dtype=int)
    for a, z in zip(column_count, R[:, 1:].T):
        v, c = np.unique(z, return_counts=True)
        a[v] = c
    counts = np.cumsum(column_count[::-1], axis=0)[::-1]
    ent = entropy(counts, base=2, axis=-1)
    ds = np.ceil(ent*(10**14)) % n
    ds = np.concatenate([ds, [0]]).astype(int)

    for i, d in enumerate(ds):
        if i == 0:
            C[:, i] = (R[:, i]+(d+1)*K[:, i]+K[:, d]) % 256
        else:
            C[:, i] = (R[:, i]+(d+1)*C[:, i-1]+(d+1)*K[:, i]+K[:, d]) % 256
    return C

if __name__ == '__main__':
    print('Generating new key and flag (260x260)...')
    GenerateNewKey()
    F = GenerateNewFlag()
    C = Encrypt(F)
    print('Encrypted flag (flag.bmp):')
    print(base64.b64encode(C.tostring()).decode())
    I = GetSameEntropyImage(F)
    print('Image with the same entropy (image.bmp):')
    print(base64.b64encode(I.tostring()).decode())
    for i in range(1200):
        M = int(input('Gimme the image size M> '))
        N = int(input('Gimme the image size N> '))
        if 256 <= M <= 512 and 256 <= N <= 512:
            img_str = base64.b64decode(input('Gimme the base64 encoded image> '))
            A = np.fromstring(img_str, np.uint8)
            A = A.reshape(M, N)
            C = Encrypt(A)
            print(base64.b64encode(C.tostring()).decode())
        else:
            print('Invalid size!')

