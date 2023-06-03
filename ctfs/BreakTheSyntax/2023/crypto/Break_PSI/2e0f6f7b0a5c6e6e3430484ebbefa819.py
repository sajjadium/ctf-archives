from Crypto.Hash import SHA256
from Crypto.Util.number import long_to_bytes
import random

FLAG = open("flag", "r")

A = []
B = []
Ahash = []
Bhash = []
Ainv = {}
Binv = {}

limit = 32
setSize = 17
reps = 8


def intersection(A, B):
    return [v for v in A if v in B]


def F(x):
    h = SHA256.new(data=long_to_bytes(x))
    return h.digest().hex()


def hash_list(l):
    h = SHA256.new(data=bytes(str(l), "utf-8"))
    return h.digest()


def is_valid(Asi, Bsi):
    if Asi == [] or Bsi == []:
        return 0
    if hash_list(Asi) != hash_list(Bsi):
        return 0

    cnt = {}
    for a in Asi:
        if Ainv[a] in cnt:
            cnt[Ainv[a]] += 1
        else:
            cnt[Ainv[a]] = 1
    for v in cnt.values():
        if v != reps + 1:
            return 0

    cnt = {}
    for b in Bsi:
        if Binv[b] in cnt:
            cnt[Binv[b]] += 1
        else:
            cnt[Binv[b]] = 1
    for v in cnt.values():
        if v != reps + 1:
            return 0

    return 1


for i in range(420):
    A = random.sample(range(limit), setSize)
    B = random.sample(range(limit), setSize)
    Ahash = []
    Bhash = []
    Ainv = {}
    Binv = {}

    for i in range(setSize):
        for j in range(1, reps + 1):
            A.append(A[i] + limit * j)
            B.append(B[i] + limit * j)

    for a in A:
        h = F(a)
        Ahash.append(h)
        Ainv[h] = a % limit

    for b in B:
        h = F(b)
        Bhash.append(h)
        Binv[h] = b % limit

    print("Alice:", Ahash)
    print("Bob:", Bhash)

    Asi = input("Send PSI to Alice: ").split()
    Bsi = input("Send PSI to Bob: ").split()

    if is_valid(Asi, Bsi):
        if intersection(Ahash, Bhash) == Asi and intersection(Ahash, Bhash) == Bsi:
            print("Honesty is not a way to solve this challenge")
            exit()
    else:
        print("Cheater!")
        exit()

print("You got me! Here is your flag:", FLAG.read())
