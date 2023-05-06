#!/usr/bin/env python3

# Hash constants
A = 340282366920938460843936948965011886881
B = 127605873542257115442148455720344860097

# Hash function
def H(val, prev_hash, hash_num):
    return (prev_hash * pow(val + hash_num, B, A) % A)


if __name__ == "__main__":

    # Print welcome message
    print("Welcome to TrashChain!")
    print("In this challenge, you will enter two sequences of integers which are used to compute two hashes. If the two hashes match, you get the flag!")
    print("Restrictions:")
    print("  - Integers must be greater than 1.")
    print("  - Chain 2 must be at least 3 integers longer than chain 1")
    print("  - All integers in chain 1 must be less than the smallest element in chain 2")
    print("Type \"done\" when you are finished inputting numbers for each chain.")

    # Get inputs
    chains = [[], []]
    for chain_num in range(len(chains)):
        print("\nProvide inputs for chain {}.".format(chain_num+1))
        while True:
            val = input("> ")
            if val == "done":
                break
            try:
                val = int(val)
            except ValueError:
                print("Invalid input, exiting...")
                exit(0)
            if val <= 1:
                print("Inputs must be greater than 1, exiting...")
                exit(0)
            chains[chain_num].append(val)

    # Validate chain lengths
    if not len(chains[0]):
        print("Chain 1 cannot be empty, exiting...")
        exit(0)
    if len(chains[1]) - len(chains[0]) < 3:
        print("Chain 2 must contain at least 3 more integers than chain 1, exiting...")
        exit(0)
    if max(chains[0]) >= min(chains[1]):
        print("No integer in chain 1 can be greater than the smallest integer in chain 2, exiting...")
        exit(0)

    # Compute hashes
    hashes = []
    for chain_num in range(len(chains)):
        cur_hash = 1
        for i, val in enumerate(chains[chain_num]):
            cur_hash = H(val, cur_hash, i+1)
        hashes.append(cur_hash)

    # Print hashes
    print("Hash for chain 1: {0:0{1}x}".format(hashes[0], 32))
    print("Hash for chain 2: {0:0{1}x}".format(hashes[1], 32))
    if hashes[0] == hashes[1]:
        print("Correct! Here's your flag: DogeCTF{not_a_real_flag}")
