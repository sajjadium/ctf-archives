from graph import *
import json

G0 = random_graph(128,256)

i = random_isomorphism(G0)

while G0.is_automorphism(i):
    G0 = random_graph(128,256)
    i = random_isomorphism(G0)


with open("private_key.json","w") as f:
    f.write(json.dumps({
        "base": G0.to_dict(),
        "transformation": str(i)
    }))

G1 = G0.map_vertices(i)

with open("public_key.json","w") as f:
    f.write(json.dumps(
        [
            G0.to_dict(),
            G1.to_dict()
        ]
    ))