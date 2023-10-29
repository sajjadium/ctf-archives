from random import SystemRandom
from sympy.ntheory.generate import nextprime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256

flag = b"srdnlen{????????????????????????????????????????????????????????????????????????????????????}"

n = 32
q = nextprime(int(0x1337**7.331))
random = SystemRandom()


class MPDH:
    n = n
    q = q

    def __init__(self, G=None) -> None:
        if G is None:
            J = list(range(n))
            random.shuffle(J)
            self.G = [(j, random.randrange(1, q)) for j in J]
        else:
            self.G = list(G)

    def one(self) -> "list[tuple[int, int]]":
        return [(i, 1) for i in range(self.n)]
    
    def mul(self, P1, P2) -> "list[tuple[int, int]]":
        return [(j2, p1 * p2 % self.q) for j1, p1 in P1 for i, (j2, p2) in enumerate(P2) if i == j1]
    
    def pow(self, e: int) -> "list[tuple[int, int]]":
        if e == 0:
            return self.one()
        if e == 1:
            return self.G
        P = self.pow(e // 2)

        P = self.mul(P, P)
        if e & 1:
            P = self.mul(P, self.G)
        return P


mpdh = MPDH()

a = random.randrange(1, q - 1)
A = mpdh.pow(a)

b = random.randrange(1, q - 1)
B = mpdh.pow(b)

Ka = MPDH(G=B).pow(a)
Kb = MPDH(G=A).pow(b)
assert Ka == Kb

key = SHA256.new(str(Ka).encode()).digest()[:AES.key_size[-1]]
flag_enc = AES.new(key, AES.MODE_ECB).encrypt(pad(flag, AES.block_size))
assert flag == unpad(AES.new(key, AES.MODE_ECB).decrypt(flag_enc), AES.block_size)

print(f"G = {mpdh.G}")
print(f"{A = }")
print(f"{B = }")
print(f'flag_enc = "{flag_enc.hex()}"')
