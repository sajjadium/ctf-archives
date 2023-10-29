from graph import *
import json

with open("private_key.json","r") as f:
    key = json.loads(f.read())

G0 = Graph.from_dict(key["base"])
d = Isomorphism.loads(G0,key["transformation"])
G1 = G0.map_vertices(d)

print(G0.dumps())
print(G1.dumps())

G2 = Graph.loads(input().strip())

i = Isomorphism.loads(G2,input().strip())

if G2.is_automorphism(i):
    raise ValueError("Nice try!")
if not G2.check_mapping(G0,i):
    raise ValueError("The given mapping does not map the provided graph to G0!")

m = i + d

print(m)

auth = input().strip()

if auth == "y":
    print("give me the flag")