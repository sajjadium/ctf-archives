from lib import GES, utils
import networkx as nx
import random

from SECRET import flag, get_SDSP_node_degrees

'''
get_SDSP_node_degrees(G, dest) returns the node degrees in the single-destination shortest path (SDSP) tree, sorted in ascending order.
For example, if G has 5 nodes with edges (1,2),(1,3),(2,3),(2,5),(4,5) and dest=1, returns "1 1 2 2 2".
[+] Original:       [+] SDSP:
1--2--5--4          1--2--5--4
| /                 |
3                   3
'''
# Another example for sanity check
TestGraph = utils.generate_graph([[1, 2], [1, 4], [1, 6], [6, 5], [6, 7], [4, 7], [2, 5]])
assert get_SDSP_node_degrees(TestGraph, 1) == '1 1 1 2 2 3'

NODE_COUNT = 130
EDGE_PROB = 0.031
SECURITY_PARAMETER = 32

def gen_random_graph() -> nx.Graph:
    return nx.fast_gnp_random_graph(n=NODE_COUNT, p=EDGE_PROB)

if __name__ == '__main__':
    try:
        print("[!] Pass 10 challenges to get the flag:")
        for q in range(10):
            print(f"[+] Challenge {q+1}/10. Generating random graph...")
            while True:
                G = gen_random_graph()
                if nx.is_connected(G):
                    break
            myGES = GES.GESClass(cores=4, encrypted_db={})
            key = myGES.keyGen(SECURITY_PARAMETER)

            print("[+] Encrypting graph...")
            enc_db = myGES.encryptGraph(key, G)

            dest = random.choice(list(G.nodes()))
            print(f"[*] Destination: {dest}")

            attempts = NODE_COUNT
            while attempts > 0:
                attempts -= 1
                query = input("> Query u,v: ").strip()
                try:
                    u, v = map(int, query.split(','))
                    assert u in G.nodes() and v in G.nodes() and u != v
                except:
                    print("[!] Invalid query!")
                    break
                token = myGES.tokenGen(key, (u, v))
                print(f"[*] Token: {token.hex()}")
                tok, resp = myGES.search(token, enc_db)
                print(f"[*] Query Response: {tok.hex() + resp.hex()}")

            ans = input("> Answer: ").strip()
            if ans != get_SDSP_node_degrees(G, dest):
                print("[!] Wrong answer!")
                exit()
        print(f"[+] Flag: {flag}")
    except:
        exit()