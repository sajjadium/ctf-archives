from sympy import Matrix
from math import ceil

def pad(pt: str, m: int) -> str:
    n = len(pt)
    pt += '-' * (m * ceil(n/m) - n)

    return pt

def enc_affine_hill(pt: str, m: int, K: Matrix, b: Matrix) -> str:
    n = len(pt)
    pt_padded = pad(pt, m)
    pt_vecs = [list(map(lambda x: alphabet.index(x), pt_padded[m*i:m*(i+1)])) for i in range(n//m)]

    ct = ""
    for pt_vec in pt_vecs:
        pt_vec = Matrix(pt_vec).T
        ct_vec = list((pt_vec * K + b) % l)
        ct_block = ''.join(map(lambda x : alphabet[x], ct_vec))
        ct += ct_block

    return ct

pt = "b3w4reofbugs1ntheab0vec0de-ih4ve0nlyprov3ditc0rrectnottr13dit"
n = len(pt)
alphabet = "abcdefghijklmnopqrstuvwxyz0123456789-"
l = len(alphabet)
m = 4

with open('gaslight-affine-hill/keywords.txt') as file:
    keyword1 = file.readline().strip()
    keyword2 = file.readline().strip()

K1 = Matrix([list(map(lambda x : alphabet.index(x), keyword1[:-m][m*i:m*(i+1)])) for i in range(m)])
b1 = Matrix(list(map(lambda x : alphabet.index(x), keyword1[-m:]))).T
K2 = Matrix([list(map(lambda x : alphabet.index(x), keyword2[:-m][m*i:m*(i+1)])) for i in range(m)])
b2 = Matrix(list(map(lambda x : alphabet.index(x), keyword2[-m:]))).T

ct1 = enc_affine_hill(pt, m, K1, b1)
ct2 = enc_affine_hill(pt, m, K2, b2)

print(f"Padded plaintext: {pad(pt, m)}")
print(f"Ciphertext with key 1: {ct1}")
print(f"Ciphertext with key 2: {ct2}")
