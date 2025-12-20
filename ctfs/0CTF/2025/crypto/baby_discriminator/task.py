import random
from hashlib import md5, sha256
import secrets
import string
import numpy as np
import sys

try:
    from secret import flag
except ImportError:
    flag = "0ops{this_is_a_test_flag}"

window = 5
total_nums = 20000
vector_size = 140


def proof_of_work():
    challenge = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
    difficulty = 6
    print(f"Proof of Work challenge:")
    print(f"sha256({challenge} + ???) starts with {'0' * difficulty}")
    
    sys.stdout.write("Enter your answer: ")
    sys.stdout.flush()
    answer = sys.stdin.readline().strip()
    
    hash_res = sha256((challenge + answer).encode()).hexdigest()
    if hash_res.startswith('0' * difficulty):
        return True
    return False


def choose_one(seed = None):
    p_v = 10 ** np.random.uniform(0, 13, size=total_nums)
    if seed is not None:
        seed_int = int(seed, 16)
        rng = np.random.default_rng(seed_int)
    else:
        rng = np.random.default_rng()
        
    us = rng.random(total_nums)
    return int(np.argmax(np.log(us) / p_v))


def get_vector(bit):
    if bit == 0:
        v = []
        for _ in range(vector_size):
            seed = md5(str(v[-window:]).encode()).hexdigest() if len(v) >= window else None
            v.append(choose_one(seed))
        
        to_change = secrets.randbelow(65)
        pos = random.choices(range(vector_size), k=to_change)
        for p in pos:
            v[p] = choose_one()
        return v
    else:
        return [choose_one() for _ in range(vector_size)]

if not proof_of_work():
    print("PoW verification failed!")
    exit()

banner = """
 █████   ███   █████          ████  ████                                        █████                   █████      █████████  ███████████ ███████████
░░███   ░███  ░░███          ░░███ ░░███                                       ░░███                  ███░░░███   ███░░░░░███░█░░░███░░░█░░███░░░░░░█
 ░███   ░███   ░███   ██████  ░███  ░███   ██████   ██████  █████████████      ███████    ██████     ███   ░░███ ███     ░░░ ░   ░███  ░  ░███   █ ░ 
 ░███   ░███   ░███  ███░░███ ░███  ░███  ███░░███ ███░░███░░███░░███░░███    ░░░███░    ███░░███   ░███    ░███░███             ░███     ░███████   
 ░░███  █████  ███  ░███████  ░███  ░███ ░███ ░░░ ░███ ░███ ░███ ░███ ░███      ░███    ░███ ░███   ░███    ░███░███             ░███     ░███░░░█   
  ░░░█████░█████░   ░███░░░   ░███  ░███ ░███  ███░███ ░███ ░███ ░███ ░███      ░███ ███░███ ░███   ░░███   ███ ░░███     ███    ░███     ░███  ░    
    ░░███ ░░███     ░░██████  █████ █████░░██████ ░░██████  █████░███ █████     ░░█████ ░░██████     ░░░█████░   ░░█████████     █████    █████      
     ░░░   ░░░       ░░░░░░  ░░░░░ ░░░░░  ░░░░░░   ░░░░░░  ░░░░░ ░░░ ░░░░░       ░░░░░   ░░░░░░        ░░░░░░     ░░░░░░░░░     ░░░░░    ░░░░░       
"""

print(banner)
print("Are u ready to play the game")

play_times = 200
for i in range(play_times):
    bit = secrets.randbelow(2)
    v = get_vector(bit)
    print("Vector: ", v)
    print("Please tell me the bit of the vector")
    try:
        user_bit = int(input())
    except ValueError:
        print("Invalid input")
        exit()
        
    if user_bit != bit:
        print("Wrong answer")
        exit()

print("You are a good guesser, the flag is ", flag)