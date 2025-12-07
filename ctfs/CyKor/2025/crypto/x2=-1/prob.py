#!/usr/bin/python3
import math
import os
import signal
from Crypto.Util.number import *
from hashlib import sha256

##### PARAMS #####
P = 2**47 - 297 # Field size
N = 256 # Number of parties
kappa = 64 # Security parameter
tau = 50 # Number of repetitions
##################

# No more suffering from MTU/slow interaction !!
def input_list(name, size):
    ret = []
    while len(ret) < size:
        ret += input(f'{name} > ').split(',')
    return ret[:size]

def H(SALT, domain, party_index, SEED):
    msg = b'Cykor' + SALT + bytes([domain, party_index]) + SEED
    return bytes_to_long(sha256(msg).digest()) % P

def init():
    print('================================================================================')
    print('Prove your knowledge of x such that x^2 = -1 (mod P), without revealing x itself')
    print('================================================================================')

def protocol(SALT, rounds, target):
    ### Round 1 : Committing to the seeds and views of the parties
    Delta_c = int(input("Δc = "))
    Delta_x = int(input("Δx = "))

    ### Round 2 : Challenging the checking protocol
    r = bytes_to_long(os.urandom(6)) % P
    print(f"{r = }")

    ### Round 3 : Commit to simulation of the checking protocol
    alpha_share = input_list('alpha_shares', N)
    alpha_share = [int(x) for x in alpha_share]
    beta_share = input_list('beta_shares', N)
    beta_share = [int(x) for x in beta_share]
    v_share = input_list('v_shares', N)
    v_share = [int(x) for x in v_share]
        
    alpha = sum(alpha_share) % P
    beta = sum(beta_share) % P
    v = sum(v_share) % P

    ### Round 4 : Challenging the views of the MPC protocol
    i_bar = bytes_to_long(os.urandom(1))
    print(f"{i_bar = }")

    ### Round 5 : Opening the views of the MPC and checking protocols.
    # Note that seeds[i_bar] is unused in below check routine.
    seeds = input_list('seeds', N)
    seeds = [bytes.fromhex(x) for x in seeds]

    # Now the interactive between user is done,
    # server vefifies it.

    # Generate shares of beaver triple (a, b, c)
    # and input share x (except i_bar)
    a_share = [0] * N
    b_share = [0] * N
    c_share = [0] * N
    x_share = [0] * N
    
    for i in range(N):
        if i == i_bar:
            continue
        a_share[i] = H(SALT, 0, i, seeds[i])
        b_share[i] = H(SALT, 1, i, seeds[i])
        c_share[i] = H(SALT, 2, i, seeds[i])
        x_share[i] = H(SALT, 3, i, seeds[i])

    # Adjust c_share[0] and x_share[0] using Δc and Δx.
    # A prover provides honest adjust values, I guess....?
    c_share[0] = (c_share[0] + Delta_c) % P
    x_share[0] = (x_share[0] + Delta_x) % P

    # If x^2 == target and c == ab, then z = 0.

    # 1. Check whether v == 0
    if v != 0:
        return False

    # 2. Check whether shares of alpha, beta, and v are valid
    for i in range(N):
        if i == i_bar:
            continue

        # Validity of alpha share
        alpha_verify = (r * x_share[i] + a_share[i]) % P
        if alpha_verify != alpha_share[i]:
            return False

        # Validity of beta share
        beta_verify = (x_share[i] + b_share[i]) % P
        if beta_verify != beta_share[i]:
            return False

        # Validity of v share
        v_verify = 0
        if i == 0:
            v_verify = (r*target - c_share[i] + alpha * b_share[i] + beta * a_share[i] - alpha * beta) % P
        else:
            v_verify = (-c_share[i] + alpha * b_share[i] + beta * a_share[i]) % P
        if v_verify != v_share[i]:
            return False
        
    return True

if __name__ == '__main__':
    signal.alarm(1800)
    init()

    SALT = os.urandom(kappa // 4)
    print(f"SALT = {SALT.hex()}")

    for i in range(tau):
        print(f"===== {i+1}/{tau} =====\n")
        if not protocol(SALT, rounds = i, target = P-1):
            print("bye...")
            break
        print("ok, cool!")

    else:
        flag = open("flag", "rb").read()
        print(flag)