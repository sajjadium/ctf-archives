from Crypto.Util.number import getPrime, getRandomNBitInteger
import os

FLAG = os.getenv("FLAG", "RicSec{*** REDACTED ***}").encode()

def RSALCG(a, b, n):
    e = 65537
    s = getRandomNBitInteger(1024) % n
    while True:
        s = (a * s + b) % n
        yield pow(s, e, n)

def encrypt(rand, msg):
    assert len(msg) < 128
    m = int.from_bytes(msg, 'big')
    return int.to_bytes(m ^ next(rand), 128, 'big')

if __name__ == '__main__':
    n = getPrime(512) * getPrime(512)
    a = getRandomNBitInteger(1024)
    b = getRandomNBitInteger(1024)
    rand = RSALCG(a, b, n)
    print(f"{a = }")
    print(f"{b = }")
    print(f"{n = }")
    print(encrypt(rand, b"The quick brown fox jumps over the lazy dog").hex())
    print(encrypt(rand, FLAG).hex())
    print(encrypt(rand, b"https://translate.google.com/?sl=it&tl=en&text=ricerca").hex())
