import graph
import json
import random

RAND = random.SystemRandom()

def generate_tree(depth: int, root, vertices, edges):
    if depth == 0:
        return
    else:
        size = RAND.randint(0,4)
        if size > len(vertices):
            return
        children = random.sample(list(vertices),size)
        for child in children:
            vertices.remove(child)
            edges.add((root, child))
        for child in children:
            generate_tree(depth-1,child,vertices,edges)

def random_graph(size: int = 128, max_depth = 3):
    vertices = set(range(size))
    edges = set()
    for _ in range(RAND.randint(2,size//10)):
        if len(vertices) == 0:
            break
        root = random.choice(list(vertices))
        vertices.remove(root)
        generate_tree(RAND.randint(1,max_depth),root,vertices,edges)
    return graph.Graph(range(size),edges)


G0 = random_graph()
i = graph.random_isomorphism(G0)

while G0.is_automorphism(i):
    G0 = random_graph()
    i = graph.random_isomorphism(G0)


with open("private_key.json","w") as f:
    f.write(json.dumps({
        "base": G0.to_dict(),
        "transformation": i._mapping
    }))

G1 = G0.map_vertices(i)

with open("public_key.json","w") as f:
    f.write(json.dumps(
        [
            G0.to_dict(),
            G1.to_dict()
        ]
    ))