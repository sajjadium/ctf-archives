#!/usr/local/bin/python

from hamiltonicity import pedersen_commit, pedersen_open
from hamiltonicity import open_graph, permute_graph
from hamiltonicity import testcycle, check_graph
from hamiltonicity import comm_params
import json
import random

FLAG = open("flag.txt").read()
numrounds = 128

N = 5
payload = json.loads(input("send graph G: "))
G = payload["G"]
check_graph(G, N)

# how are you going to have a hamiltonian cycle if there aren't even enough edges in the graph :3c
if not all(g in [0, 1] for g_ in G for g in g_):
    print("this graph doesn't look quite right...")
    exit()

if not sum([g for g_ in G for g in g_]) < N:
    print("hey, that's too many edges in your graph...")
    exit()

print(f'now, prove that G has a hamiltonian cycle!')

for i in range(numrounds):
    print(f"round {i + 1}")
    
    payload = json.loads(input("send commitment A: "))
    A = payload["A"]
    check_graph(A,N)
    
    challenge = random.randint(0, 1)
    print(f"challenge bit is {challenge}")
    
    payload = json.loads(input("send proof z: "))
    z = payload["z"]
    
    # Challenge bit is 1:
    # You should open the hamiltonian path
    # z = [cycle, openings of cycle]
    if challenge:
        cycle, openings = z
        if not testcycle(A, N, cycle, openings):
            print("i'm not satisfied with your proof...")
            exit()
    
    # challenge bit is 0:
    # you should show permutation and open everything
    # z = [permutation, openings of everything]
    else:
        permutation, openings = z
        G_permuted = open_graph(A, N, openings)
        G_test = permute_graph(G, N, permutation)
        if G_permuted != G_test:
            print("i'm not satisfied with your proof...")
            exit()

print("okay, i'm satisfied now... have your flag")
print(FLAG)