import hashlib

ROUNDS = 25
BLOCKSIZE = 32

def xor(a, b):
    assert len(a) == len(b)
    return bytes(x ^ y for x, y in zip(a, b))

def F(x):
    return hashlib.sha256(x).digest()

def round(x):
    assert len(x) == 2 * BLOCKSIZE
    L = x[:BLOCKSIZE]
    R = x[BLOCKSIZE:]
    return R + xor(L, F(R))

def encrypt(x):
    for _ in range(ROUNDS):
        x = round(x)
    return x

if __name__ == "__main__":
    flag = open("flag.txt", "rb").read().strip()
    open("output.txt", "w").write(encrypt(flag).hex())
