import os
import time
FLAG = os.getenv("FLAG", "ASCWG{XXXX}").encode()

def gen_prime():
    while True:
        p = 2
        for _ in range((2<<2)+1):
            p *= getrandbits(58)
        if is_prime(p+1):
            return p+1

def encrypt():
    x = G(getrandbits(256))
    h = g^x
    y = G.random_element()
    s = h^y
    c1 = g^y
    m = G(int.from_bytes(FLAG, byteorder="big"))
    c2 = m*s
    return (q, g, h, c1, c2), x

if __name__ == "__main__":
    q = gen_prime()
    G = GF(q, modulus="primitive")
    g = G.gen()
    print(encrypt()[0])