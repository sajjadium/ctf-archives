from Crypto.Util.number import isPrime
from random import randrange
from secret import p, q, L, e, d

class RSA:
    def __init__(self, p, q, L, e, d):
        assert(isPrime(p) and isPrime(q))
        self.N = p * q
        self.L = L
        self.e = e
        self.d = d

        # these are the normal RSA conditions
        for _ in range(100):
            assert(pow(randrange(1, self.N), self.L, self.N) == 1)
        assert(self.e * self.d % self.L == 1)

        # minimal is the best
        assert(self.L * self.L <= 10000 * self.N)

    def gen_private_key(self):
        return (self.N, self.d)

    def gen_public_key(self):
        return (self.N, self.e)

    def encrypt(self, msg):
        return pow(msg, self.e, self.N)

    def decrypt(self, c):
        return pow(c, self.d, self.N)

flag = open('flag.txt', 'rb').read()
msg = int.from_bytes(flag, byteorder='big')
assert(msg < p * q)

rsa = RSA(p, q, L, e, d)
encrypted = rsa.encrypt(msg)
assert(rsa.decrypt(encrypted) == msg)

print(f'N, e = {rsa.gen_public_key()}')
print(f'c = {encrypted}')
