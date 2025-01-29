from hashlib import sha256
from tqdm import tqdm

rubik_moves = "B' U  B' R  F2 "
P = Permutation(eval(open("permutation.txt").read())).to_permutation_group_element()
forbidden = [2, 27, 45, 56, 70, 86, 94, 138, 140, 167, 182, 232, 283, 284, 306, 308, 335, 348, 350, 363, 378, 423, 428, 446, 452, 506, 507, 536, 544, 560, 578, 579, 585, 587, 590, 592, 619, 642, 670, 675, 702, 731, 732, 738, 758, 760, 768, 770, 782, 783, 814, 830, 834, 843, 862, 867, 927, 936, 952, 980, 1010, 1038, 1091, 1119, 1148, 1150, 1152, 1170, 1174, 1175, 1188, 1190, 1204, 1206, 1222]
n = 641154303900

def spicy_rubik_pow(k):
    C = RubiksCube().move(rubik_moves * (k % 1260))
    
    return (P * C._state)**k

def hash_to_int(m):
    return int(sha256(m.encode()).hexdigest(), 16) % n

def sign(msg, d):
    k = n
    r_hash = n

    while gcd(k, n) != 1 or gcd(r_hash, n) != 1 or (k % 1260) in forbidden:
        k = randint(2, n - 1)
        r = spicy_rubik_pow(k)
        r_hash = hash_to_int(str(r))
    
    s = pow(k, -1, n) * (hash_to_int(msg) + r_hash*d) % n

    return r, s

flag = b"MVM{_fakemvmfakemvm_}"
flag = flag[4:-1]
privkeys = [randint(0, n) for i in range(32)]

assert len(flag) == 16

out = open("out.txt", "w")

for i in range(32):
    r,s = sign(f"mvm_{i}", privkeys[i])

    out.write(str(r) + "\n")
    out.write(str(s) + "\n")

for i in range(0, len(flag), 4):
    secret = vector([flag[i + j] for j in range(4)])
    ds = vector(privkeys[i:i+4])

    out.write(str(secret * ds) + "\n")