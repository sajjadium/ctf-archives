import json
from graph import Graph, Isomorphism
import typing
import os

ROUNDS = 16

with open("public_key.json",'r') as f:
    key = list(map(Graph.from_dict,json.load(f)))

with open("flag.txt",'r') as f:
    flag = f.read()

def authenticate(key: typing.List[Graph]):
    Graphs = [Graph.from_dict(json.loads(input().strip())) for _ in range(ROUNDS)]
    challenges = os.urandom((ROUNDS//8)+1 if ROUNDS % 8 != 0 else ROUNDS//8)
    print(challenges.hex())
    challenges = int.from_bytes(challenges,'big')
    for G2 in Graphs:
        challenge = challenges % 2
        tau = Isomorphism.loads(G2,input().strip())
        if not key[challenge].check_mapping(G2,tau):
            return False
        challenges >>= 1
    return True

try:
    if authenticate(key):
        print("y")
        print(flag)
    else:
        print("n")
except:
    print("n")



