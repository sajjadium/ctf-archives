from lib import GES, utils
import networkx as nx
import random

from SECRET import flag, decrypt

NODE_COUNT = 130
EDGE_COUNT = 260
SECURITY_PARAMETER = 16

def gen_random_graph(node_count: int, edge_count: int) -> nx.Graph:
    nodes = [i for i in range(1, node_count + 1)]
    edges = []
    while len(edges) <  edge_count:
        u, v = random.choices(nodes, k=2)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.append([u, v])
    return utils.generate_graph(edges)

if __name__ == '__main__':
    try:
        print("[+] Generating random graph...")
        G = gen_random_graph(NODE_COUNT, EDGE_COUNT)
        myGES = GES.GESClass(cores=4, encrypted_db={})
        key = myGES.keyGen(SECURITY_PARAMETER)
        print(f"[*] Key: {key.hex()}")

        print("[+] Encrypting graph...")
        enc_db = myGES.encryptGraph(key, G)

        print("[!] Answer 50 queries to get the flag. In each query, input the shortest path \
              decrypted from response. It will be a string of space-separated nodes from \
              source to destination, e.g. '1 2 3 4'.")
        for q in range(50):
            while True:
                u, v = random.choices(list(G.nodes), k=2)
                if nx.has_path(G, u, v):
                    break
            print(f"[+] Query {q+1}/50: {u} {v}")
            token = myGES.tokenGen(key, (u, v))
            _, resp = myGES.search(token, enc_db)
            print(f"[*] Response: {resp.hex()}")

            ans = input("> Original query: ").strip()
            if ans != decrypt(u, v, resp, key):
                print("[!] Wrong answer!")
                exit()
        print(f"[+] Flag: {flag}")
    except:
        exit()