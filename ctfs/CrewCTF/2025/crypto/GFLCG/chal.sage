from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class LCG:
    def __init__(self, nbits):
        self.nbits = nbits
        R = GF(2)['x']
        mod = 0
        while True:
            mod = R.random_element(degree=nbits)
            if mod.is_irreducible():
                break
        assert mod.degree() == nbits
        self.F = GF(2 ** nbits, 'x', modulus=mod)
        self.a = self.F.random_element()
        self.b = self.F.random_element()
        self.m = mod
        self.state = self.F.random_element()

    def __next__(self):
        self.state *= self.a
        self.state += self.b
        return self.state.to_integer() >> ((self.nbits * 2) // 3)


L = LCG(64 * 3)

values = [next(L) for _ in range(200)]
print(f'{values = }')

v1 = next(L)
v2 = next(L)
key = v1 + v2 * pow(2, 64)
key = int.to_bytes(int(key), 16)

flag = 'crew{*** REDACTED ***}'
cipher = AES.new(key, AES.MODE_ECB)

msg = cipher.encrypt(pad(flag.encode(), 16))
print(f'{msg = }')
