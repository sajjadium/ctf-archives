import os
import hashlib
import random

DEFAULT_DIFFICULTY = int(os.environ.get('DEFAULT_DIFFICULTY', 6))
DEFAULT_INPUT_LENGTH = int(os.environ.get('DEFAULT_INPUT_LENGTH', 13))


check = lambda s, challenge, prefix: hashlib.sha256((challenge + s).encode('utf-8')).hexdigest()[:len(prefix)] == prefix

def solve_pow(challenge, prefix):
    for i in range(0, 2**32):
        if check(str(i), challenge, prefix):
            return challenge + str(i)
    return -1


def challenge_proof_of_work(): # out of scope for the challenge
    input_prefix = ''.join(random.choice('0123456789abcdef') for _ in range(DEFAULT_INPUT_LENGTH))
    hash_prefix = ''.join(random.choice('0123456789abcdef') for _ in range(DEFAULT_DIFFICULTY))

    print(f'Please provide a string that starts with {input_prefix} and whose sha256 hash starts with {hash_prefix}')
    print('Example Python implementation: check = lambda s, challenge, prefix: hashlib.sha256((challenge + s).encode("utf-8")).hexdigest()[:len(prefix)] == prefix')
    answer = input("POW: >")
    answer = answer.strip()
    if not answer.startswith(input_prefix):
        print(f'Input does not start with {input_prefix}!')
        return False
    h = hashlib.new("sha256")
    h.update(answer.encode('utf-8'))
    hashed_value = h.hexdigest()
    if not hashed_value.startswith(hash_prefix):
        print(f'Hash does not start with {hash_prefix}!')
        return False
    return True
