from Crypto.Util.number import getPrime, bytes_to_long
from random import randint
from SECRET import FLAG

def key_gen():
    ps = []
    n = randint(2,2**6)
    for _ in range(n):
        p = getPrime(256)
        ps.append(p)
    return ps

def encrypt(m, ps):
    ps.sort()
    for p in ps:
        e = 1<<1
        m = pow(m, e, p)
    return m

if __name__ == "__main__":
    ps = key_gen()
    c = encrypt(bytes_to_long(FLAG), ps)
    print('ps = {}\nc = {}'.format(ps, c))