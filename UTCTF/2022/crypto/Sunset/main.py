import random
import hashlib


N = 111
MOD = 10**9+7

def get_secret_key():
    key = []
    for i in range(1, N):
        x = random.randrange(1,10)
        key += [i] * x
    random.shuffle(key)
    return key

def compute_arr(arr, sk):
    for x in sk:
        new_arr = arr.copy()
        for y in range(N):
            new_arr[(x+y)%N] += arr[y]
            new_arr[(x+y)%N] %= MOD

        arr = new_arr
    return arr

def compute_public_key(sk):
    arr = [0] * N
    arr[0] = 1
    return compute_arr(arr, sk)

A_sk = get_secret_key()
B_sk = get_secret_key()

A_pk = compute_public_key(A_sk)
B_pk = compute_public_key(B_sk)

print("Alice's public key:", A_pk)
print("Bob's public key:", B_pk)

remove_elements = random.sample(range(1,N), 20)

print("Remove: ", remove_elements)

for x in remove_elements:
    A_sk.remove(x)
    B_sk.remove(x)

A_shared = compute_arr(B_pk, A_sk)
B_shared = compute_arr(A_pk, B_sk)

assert(A_shared == B_shared)

key = hashlib.sha256(str(A_shared).encode('utf-8')).hexdigest()
print(key)
