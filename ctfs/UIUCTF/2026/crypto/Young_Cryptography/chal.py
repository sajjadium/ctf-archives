from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.number import *
from Crypto.Util.Padding import pad, unpad
from os import urandom
import random

N = 64
n = 256
flag = "uiuctf{redacted}"

def my_prod(A, B):
    n = len(A)
    z = (0,) * n

    def f(a, b, c, x):
        return (max(b[0], c[0]) + x,) + tuple(
            min(b[k-1], c[k-1]) + max(b[k], c[k]) - a[k-1]
            for k in range(1, n)
        )

    r = [z] * (n + 1)
    for row in A + B:
        s = [z]
        for j, x in enumerate(row, 1):
            s.append(f(r[j-1], r[j], s[-1], x))
        r = s

    p = [[None] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        p[i][n] = r[i]

    C = [[0] * n for _ in range(n)]
    for i in range(n-1, -1, -1):
        for j in range(n-1, i-1, -1):
            b = p[i][j+1]
            c = p[i+1][j] if i < j else b
            d = p[i+1][j+1]

            C[i][j] = C[j][i] = d[0] - max(b[0], c[0])
            p[i][j] = tuple(
                min(b[k], c[k]) +
                (max(b[k+1], c[k+1]) - d[k+1] if k+1 < n else 0)
                for k in range(n)
            )

    return C

def random_matrix():
    M = [[0] * N for _ in range(N)]
    for _ in range(n // 2):
        i, j = sorted([random.randrange(N), random.randrange(N)])
        M[i][j] += 1
        M[j][i] += 1
    return M

G = random_matrix()

# The Princess 
A = random_matrix()
AG = my_prod(A, G)

# The Enemy
B = random_matrix()
GB = my_prod(G, B)

# The Princess

AGB = my_prod(A, GB)

shared_secret = SHA256.new(str(AGB).encode()).digest()[:128]
iv = urandom(16)
cipher = AES.new(shared_secret, AES.MODE_CBC, iv)
ct = cipher.encrypt(pad(flag.encode(), 16))

print(G)
print(AG)
print(GB)
print(ct)
print(iv)
