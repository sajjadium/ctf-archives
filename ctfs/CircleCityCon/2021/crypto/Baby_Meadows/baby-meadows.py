from Crypto.Util.number import getStrongPrime
import sys, random; random.seed(0x1337)

def generate_key():
    p = getStrongPrime(2048)
    q = (p - 1) // 2
    for g in range(2, p - 1):
        if pow(g, 2, p) != 1 and pow(g, q, p) != 1:
            return g, p

def encrypt(msg):
    g, p = generate_key()

    yield (g, p)

    for m in msg:
        yield (m * pow(g, random.randrange(2, p - 1), p)) % p

if __name__ == "__main__":
    with open(sys.argv[1], "rb") as f:
        flag = f.read()
        print(list(encrypt(flag)))
