from Crypto.Util.number import getPrime, inverse, bytes_to_long
from secret import flag

assert len(flag) == 99
assert flag.startswith(b"cvctf{") and flag.endswith(b"}")

class MyRSA:
    def __init__(self, n = 2, nbits = 512):
        self.p = getPrime(nbits)
        self.q = getPrime(nbits)
        self.N = self.p * self.q
        self.d = getPrime(nbits//2 - 1)
        self.my_phi = self.gen_phi(n)
        self.e = inverse(self.d, self.my_phi)

    def gen_phi(self, n):
        return sum([self.p**i for i in range(n)]) * sum([self.q**i for i in range(n)])

    def encrypt(self, m):
        print("I am not going to encrypt anything...")
        return m

    def get_public(self):
        print(f"N = {self.N}")
        print(f"e = {self.e}\n")
    
    def get_private(self):
        # print(f"d = {self.d}")
        return self.d

NPARTS = 3
fractions = [bytes_to_long(flag[len(flag)//NPARTS*i:len(flag)//NPARTS*(i+1)]) for i in range(NPARTS)]

print("[+] Here are my public keys:")
ns = [2, 3, 6]
rsas = [MyRSA(n) for n in ns]
private_exponents = [rsa.get_private() for rsa in rsas]

for rsa in rsas:
    rsa.get_public()

print("[+] Here are my flag fractions:")
for i in range(NPARTS):
    f = sum(fractions[j] * private_exponents[i]**(NPARTS-1-j) for j in range(NPARTS))
    print(f"[!] Fraction {i+1}: {f}")
