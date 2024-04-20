from Crypto.Util.number import getPrime

with open("flag.txt",'rb') as f:
    FLAG = f.read().decode()
    f.close()


def encrypt(plaintext, mod):
    plaintext_int = int.from_bytes(plaintext.encode(), 'big')
    return pow(plaintext_int, 3, mod)


while True:
    p = [getPrime(128) for _ in range(6)]
    if len(p) == len(set(p)):
        break

N1, N2, N3 = p[0] * p[1], p[2] * p[3], p[4] * p[5]
m1, m2, m3 = encrypt(FLAG, N1), encrypt(FLAG, N2), encrypt(FLAG, N3)

pairs = [(m1, N1), (m2, N2), (m3, N3)]
for i, pair in enumerate(pairs):
    print(f'm{i+1}: {pair[0]}\nN{i+1}: {pair[1]}\n')
