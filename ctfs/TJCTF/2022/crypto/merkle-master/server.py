#!/usr/local/bin/python -u

import hashlib
import json
import random
import string
import sys
import os

with open("flag.txt") as f:
    FLAG = f.read()

N = 50
M = 1000

print("It's time for a challenge!")
print()
print("I want you to produce a sorted Merkle tree commitment for me: however,")
print("there's a catch. This needs to be a QUANTUM commitment, meaning you can")
print("prove existence or non-existence of arbitrary elements.")
print()
print("I'll also be querying random indices to make sure your tree is sorted!")
print("Don't try to pull any tricks on me!")
print()
print("Use SHA-256 and make sure your tree is a perfect tree.")
print()
print("Here's the data I care about:")
print()

required_data = []
for _ in range(N):
    data = "".join(random.choice(string.ascii_letters + string.digits) \
                   for _ in range(12))
    required_data.append(data)
    print(data)
random.shuffle(required_data)

print()
root = bytes.fromhex(input("Commitment hash: "))
depth = int(input("Tree depth: "))

seen_data_indices = {}

def prove_existence(root_hash, tree_depth, data):
    print("Give the path from root to data, with sibling hashes:")
    proof = json.loads(input())

    if len(proof) != tree_depth:
        print("Proof is wrong length!")
        return False, -1

    cur_hash = hashlib.sha256(data.encode()).digest()

    for direction, sibling_hash in proof[::-1]:
        sibling_hash = bytes.fromhex(sibling_hash)

        if len(sibling_hash) != 32:
            print("Sibling hash is wrong length!")
            return False, -1

        if direction == "L":
            cur_hash = hashlib.sha256(cur_hash + sibling_hash).digest()
        elif direction == "R":
            cur_hash = hashlib.sha256(sibling_hash + cur_hash).digest()
        else:
            print("Direction isn't L or R!")
            return False, -1

    idx = 0
    for direction, _ in proof:
        if direction == "L":
            idx = 2 * idx
        else:
            idx = 2 * idx + 1

    seen_data_indices[idx] = data

    if cur_hash != root_hash:
        print("Resulting hash doesn't match commitment!")
        return False, -1
    return True, idx


def prove_nonexistence(root, tree_depth, data):
    print("Prove the left element:")
    left_data = input("Left data: ")
    result, left_idx = prove_existence(root, tree_depth, left_data)
    if not result:
        print("Failed to prove left element!")
        return False

    print("Prove the right element:")
    right_data = input("Right data: ")
    result, right_idx = prove_existence(root, tree_depth, right_data)
    if not result:
        print("Failed to prove right element!")
        return False

    if right_idx != left_idx + 1:
        print("Elements aren't adjacent!")
        return False

    if not (left_data < data < right_data):
        print("Target data isn't lexicographically between left and right!")
        return False

    return True


# Check all the quantum commitments
for i, data in enumerate(required_data):
    # Will you be asked to prove it exists? or that it doesn't?
    # Nobody knows!
    if os.urandom(1)[0] & 1 == 1:
        print(f"Prove that '{data}' is part of your tree.")
        result, _ = prove_existence(root, depth, data)
        if not result:
            sys.exit(1)
    else:
        print(f"Prove that '{data}' is NOT part of your tree.")
        if not prove_nonexistence(root, depth, data):
            sys.exit(1)
    print("OK")
    print()


# Choose some random query indices
query_indices = [random.randrange(0, 1 << depth) for _ in range(M)]
print("Show (and prove) the data at these indices:")
print(" ".join(map(str,query_indices)))

# Query some random indices
for query_index in query_indices:
    print(f"What's at index {query_index}?")
    data = input("Data: ")
    result, idx = prove_existence(root, depth, data)
    if idx != query_index:
        print("Data isn't at the query index!")
        result = False
    if not result:
        sys.exit(1)
    print("OK")
    print()


# Verify that the tree is actually sorted
queried_indices = sorted(seen_data_indices.keys())
queried_data = [seen_data_indices[idx] for idx in queried_indices]
if not all(queried_data[i+1] >= queried_data[i] for i in range(len(queried_data)-1)):
    print("Data isn't sorted!")
    sys.exit(1)


print("Wow, I guess you really are the Merkle Master.")
print(FLAG)
