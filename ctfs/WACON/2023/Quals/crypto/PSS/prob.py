from Crypto.Util.number import *
import os
from hashlib import sha256
from tqdm import tqdm

def cascade_hash(msg, cnt, digest_len):
    assert digest_len <= 32
    msg = msg * 10
    for _ in range(cnt):
        msg = sha256(msg).digest()
    return msg[:digest_len]

def seed_to_permutation(seed):
    permutation = ''
    msg = seed + b"_shuffle"
    while len(permutation) < 16:
        msg = cascade_hash(msg, 777, 32)
        msg_hex = msg.hex()
        for c in msg_hex:
            if c not in permutation:
                permutation += c

    return permutation

def permutation_secret_sharing_gen(secret):
    seed_len = 5
    master_seed = os.urandom(seed_len)
    seed_tree = [None] * (2*N - 1)
    seed_tree[0] = master_seed
    for i in range(N-1):
        h = cascade_hash(seed_tree[i], 123, 2 * seed_len)
        seed_tree[2*i+1], seed_tree[2*i+2] = h[:seed_len], h[seed_len:]
    
    secret_list = list(secret.decode()) # ex) ['0','1','2','3',...]
    for i in range(N):
        # i-th party has a permutation derived from seed_tree[i+N-1]
        permutation = seed_to_permutation(seed_tree[i + N - 1])
        secret_list = [hex(permutation.find(x))[2:] for x in secret_list]

    permutated_secret = ''.join(secret_list)
    hidden_party = os.urandom(1)[0] & 7
    proof_idxs = merkle_proof_indexes[hidden_party]

    return seed_tree[proof_idxs[0]] + \
           seed_tree[proof_idxs[1]] + \
           seed_tree[proof_idxs[2]] + \
           bytes([hidden_party]) + \
           bytes.fromhex(permutated_secret)

merkle_proof_indexes = {
    0 : [2,4,8],
    1 : [2,4,7],
    2 : [2,3,10],
    3 : [2,3,9],
    4 : [1,6,12],
    5 : [1,6,11],
    6 : [1,5,14],
    7 : [1,5,13]
}


N = 8 # Number of parties

secret = b'---REDACTED---'
flag = b"WACON2023{" + secret + b'}'

assert len(secret) == 16 and set(secret) == set(b"0123456789abcdef")
# You can bruteforce the secret directly if you can overcome ^^^O(0xbeeeef * 16!)^^^!!!
assert cascade_hash(flag, 0xbeeeef, 32).hex() == 'f7a5108a576391671fe3231040777e9ac455d1bb8b84a16b09be1b2bac68345c'

fw = open("pss_data", "wb")
for _ in tqdm(range(2 ** 17)):
    fw.write(permutation_secret_sharing_gen(secret))

fw.close()