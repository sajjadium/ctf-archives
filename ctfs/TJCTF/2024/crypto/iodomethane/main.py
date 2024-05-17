import secrets

flag = open("flag.txt", "r").read().strip()

print(flag)

matrix = [[],[],[]]

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0192834756{}_!@#$%^&*()"

modulus = 15106021798142166691 #len(alphabet)

flag = [alphabet.index(a) for a in flag]


while len(flag) % 3 != 0:
    flag.append(secrets.randbelow(modulus))


def det(matrix):
    a = matrix[0][0]
    b = matrix[0][1]
    c = matrix[0][2]
    d = matrix[1][0]
    e = matrix[1][1]
    f = matrix[1][2]
    g = matrix[2][0]
    h = matrix[2][1]
    i = matrix[2][2]
    return ((a * e * i - a * f * h) + (b * f * g - b * d * i) + (c * d * h - c * e * g)) % modulus

def randkey():
    test = [[secrets.randbelow(modulus) for i in range(3)] for J in range(3)]
    while (not det(test)):
           test = [[secrets.randbelow(modulus) for i in range(3)] for J in range(3)]
    return test

def dot(a,b):
    return sum([a[i] * b[i] for i in range(len(a))]) % modulus

def mult(key, row):
    return [dot(key[i], row) for i in range(len(key))]

rows = list(zip(flag[::3], flag[1::3], flag[2::3]))

key = randkey()
print(key, det(key), modulus)

enc = sum([mult(key, snip) for snip in rows], start = [])
print(enc)
open("out.txt", "w+").write(str(enc))
