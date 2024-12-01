import numpy as np
from secret import flag


def gen(q, n, N, sigma):
    t = np.random.randint(0, high=q//2, size=n)
    s = np.concatenate([np.ones(1, dtype=np.int32), t])
    A = np.random.randint(0, high=q//2, size=(N, n))
    e = np.round(np.random.randn(N) * sigma ** 2).astype(np.int32) % q
    b = ((np.dot(A, t) + e).reshape(-1, 1)) % q
    P = np.hstack([b, -A])
    return P, s


def enc(P, M, q):
    N = P.shape[0]
    n = len(M)
    r = np.random.randint(0, 2, (n, N))
    Z = np.zeros((n, P.shape[1]), dtype=np.int32)
    Z[:, 0] = 1
    C = np.zeros((n, P.shape[1]), dtype=np.int32)
    for i in range(n):
        C[i] = (np.dot(P.T, r[i]) + (np.floor(q/2) * Z[i] * M[i])) % q
    return C


q = 127
n = 3
N = int(1.1 * n * np.log(q))
sigma = 1.0

P, s = gen(q, n, N, sigma)


def prep(s):
    return np.array([int(b) for char in s for b in f'{ord(char):08b}'], dtype=np.int32)


C = enc(P, prep(flag), q)
P = P.tolist()
C = C.tolist()
print(f"{P=}")
print(f"{C=}")
