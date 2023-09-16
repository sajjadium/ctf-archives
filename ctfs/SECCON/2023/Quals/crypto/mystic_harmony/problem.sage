import random
import Crypto.Cipher.AES as AES
from Crypto.Util.number import long_to_bytes
import hashlib
from flag import FLAG

R.<x, y> = PolynomialRing(GF(2))
size = 2^8
K.<alpha> = GF(size, modulus=x^8+x^4+x^3+x^2+1)

def make_human_world(human_world_size):
    H = 0
    for i in range(human_world_size):
        for j in range(human_world_size):
            H += (x^i) * (y^j) * (alpha^(random.randint(0,size-2)))
    return H

def make_spirit_world(H, spirit_world_size_param):
    Gx = prod(x-alpha^i for i in range(1,spirit_world_size_param+1))
    Gy = prod(y-alpha^i for i in range(1,spirit_world_size_param+1))
    return H % (Gx + Gy)

def make_disharmony(C, count):
    x_set = set()

    D = 0
    for i in range(count):
        r = random.randint(0,size-2)
        p = random.choice(list(C.dict().keys()))
        while p[0] in x_set:
            p = random.choice(list(C.dict().keys()))
        x_set.add(p[0])
        D += (x^p[0]) * (y^p[1]) * alpha^(r)
    return D

def make_key(D):
    key_seed = b""
    for pos, value in sorted(list(D.dict().items())):
        x = pos[0]
        y = pos[1]
        power = discrete_log(value, alpha, size-1)
        key_seed += long_to_bytes(x) + long_to_bytes(y) + long_to_bytes(power)
    m = hashlib.sha256()
    m.update(key_seed)
    return m.digest()

def get_polynomial_dict(C):
    res = C.dict()
    for key in res:
        res[key] = discrete_log(res[key], alpha, size-1)
    return res

human_world_size = 64
spirit_world_size_param = 32
disharmony_count = 16

H = make_human_world(human_world_size)
S = make_spirit_world(H, spirit_world_size_param)
World = H+S
D = make_disharmony(World, disharmony_count)
C = H+S+D

key = make_key(D)
cipher = AES.new( key, AES.MODE_ECB )

print("# Witch making the map! please wait.", flush=True)
witch_map = []
for i in range(spirit_world_size_param):
    row = []
    C_y = C(y=alpha^(i+1))
    for j in range(spirit_world_size_param):
        temp = C_y(x=alpha^(j+1))
        if temp == 0:
            row.append(None)
        else:
            row.append(discrete_log(temp, alpha, size-1))
    witch_map.append(row)
print("witch_map=", witch_map)
print("treasure_box=", cipher.encrypt(FLAG))