from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import sha256

flag = os.getenv('FLAG', 'openECSC{redacted}')

n = 10
N1 = 20
N2 = 20
L1 = 8
L2 = 11
L = 15

def patched_mul(self, other):
    ret = type(self)(self.parent(), self._data + other._data)
    # ret._normalize()
    return ret

def patched_invert(self):
    ret = type(self)(self.parent(), reversed(self._data))
    # ret._normalize()
    return ret

groups.misc.Cactus.Element._mul_ = patched_mul
groups.misc.Cactus.Element.__invert__ = patched_invert
Jn = groups.misc.Cactus(n)

s = Jn.group_generators()

def gen_elem(L1, L2):
    elem = Jn.one()
    for _ in range(randint(L1, L2)):
        p = randint(1, n-1)
        q = randint(p+1, n)
        elem *= s[p, q]
    return elem

a = [gen_elem(L1, L2) for _ in range(N1)]
b = [gen_elem(L1, L2) for _ in range(N2)]

sa = [randint(0, N1-1) for _ in range(L)]
A = prod(a[i] for i in sa)

sb = [randint(0, N2-1) for _ in range(L)]
B = prod(b[i] for i in sb)

b1 = [A**-1 * x * A for x in b]
a1 = [B**-1 * x * B for x in a]
for i in range(len(b1)):
    b1[i]._normalize()
for i in range(len(a1)):
    a1[i]._normalize()

shared_a = A**-1 * prod(a1[i] for i in sa)
shared_b = prod(b1[i] for i in sb)**-1 * B

shared_a._normalize()
shared_b._normalize()

assert shared_a == shared_b

key = sha256(str(shared_a).encode()).digest()
cipher = AES.new(key, AES.MODE_ECB)
ciphertext = cipher.encrypt(pad(flag.encode(), AES.block_size))

with open("public.txt", 'w') as wf:
    wf.write(f"{a = }\n")
    wf.write(f"{b = }\n")
    wf.write(f"{b1 = }\n")
    wf.write(f"{a1 = }\n")
    wf.write(ciphertext.hex())