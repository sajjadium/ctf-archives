import os

FLAG = os.getenv("FLAG", "ASCWG{XXXX}")

def get_prime():
    while True:
        p = 1
        for _ in range(9):
            p *= getrandbits(64)
        if is_prime(p+1):
            return p+1

def sign(M):
    S1 = int(pow(g,k,p))
    S2 = int(((M - a*S1)*inverse_mod(k,p-1))) % (p-1)
    return S1, S2

def verify(M, S1, S2):
    return pow(A,S1,p)*pow(S1,S2,p) % p == pow(g,M,p)

p = get_prime()
g = primitive_root(p)

a = secret = int.from_bytes(FLAG.encode(), "big")
A = pow(g,a,p)

k = getrandbits(256)
while gcd(k, p-1) != 1:
    k = getrandbits(256)

public = p,g,A
private = p,g,secret

print(f"Public: ", public)
while True:
    m = int.from_bytes(os.urandom(32), "big")
    S1, S2 = sign(m)
    print(S1, S2, m)

