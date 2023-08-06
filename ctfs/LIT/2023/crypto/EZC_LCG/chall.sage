from random import SystemRandom
random = SystemRandom()

def fun_prime(n): # not as smooth as my brain but should be enough
    while True:
        ps = 16
        p = 1
        for i in range(n//ps):
            p *= random_prime(2^ps)
        p += 1
        if is_prime(p):
            return p
def gen(b):
    p = fun_prime(b)
    E = EllipticCurve(GF(p), [random.randint(1, 2^b), random.randint(1,2^b)])
    return E, p, E.order()

C, p, order = gen(80)
# woah thats an lcg
class lcg:
    def __init__(self, C: EllipticCurve):
        self.order = order
        self.a = random.randint(1, self.order)
        self.x = C.gens()[0]
        self.b = self.x * random.randint(1, self.order)
    def next(self):
        self.x = (self.a * self.x + self.b)
        return self.x

prng = lcg(C)
x0 = prng.next()
x1 = prng.next()
x0, y0 = x0.xy()
x1, y1 = x1.xy()
print(f"{x0 = }")
print(f"{y0 = }")
print(f"{x1 = }")
print(f"{y1 = }")
print(f"{p = }")



from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes as l2b
from Crypto.Util.Padding import pad
from os import urandom
v = int(prng.next().xy()[0])
k = pad(l2b(v**2), 16)
iv = urandom(16)
cipher = AES.new(k, AES.MODE_CBC, iv=iv)
print(f"iv = '{iv.hex()}'")
f = open("flag.txt",'rb').read().strip()
enc = cipher.encrypt(pad(f,16))
print(f"enc = '{enc.hex()}'")
