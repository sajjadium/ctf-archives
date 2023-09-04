from itertools import product, chain
from multiprocessing import Pool
from lib import GES
import networkx as nx
import random
import time

from SECRET import flag, generate_tree, decrypt

NODE_COUNT = 60
SECURITY_PARAMETER = 128
MENU = '''============ MENU ============
1. Graph Information
2. Query Responses
3. Challenge
4. Exit
=============================='''

def query_resps(cores: int, key: bytes, G: nx.Graph, myGES: GES.GESClass, enc_db):
    n = len(G.nodes())
    query_list = []
    queries = product(set(), set())
    for component in nx.connected_components(G):
        queries = chain(queries, product(component, component))
    iterable = product([key], queries)
    chunk = n * n // cores
    
    with Pool(cores) as pool:
        for token in pool.istarmap(myGES.tokenGen, iterable, chunksize=chunk):
            tok, resp = myGES.search(token, enc_db)
            query_list.append((token.hex() + tok.hex(), resp.hex()))
    
    random.shuffle(query_list)
    return query_list

if __name__ == '__main__':
    try:
        G = generate_tree()
        assert len(G.nodes()) == NODE_COUNT
        myGES = GES.GESClass(cores=4, encrypted_db={})
        key = myGES.keyGen(SECURITY_PARAMETER)
        enc_db = myGES.encryptGraph(key, G)

        t = time.time()
        print("[!] Recover 10 queries in 30 seconds. It is guaranteed that each answer is unique.")

        while True:
            print(MENU)
            option = input("> Option: ").strip()
            if option == "1":
                print("[!] Graph information:")
                print("[*] Edges:", G.edges())
            elif option == "2":
                print(f"[*] Query Responses: ")
                resp = query_resps(4, key, G, myGES, enc_db)
                for r in resp:
                    print(f"{r[0]} {r[1]}")
            elif option == "3":
                break
            else:
                exit()

        print("[!] In each query, input the shortest path decrypted from response. \
              It will be a string of space-separated nodes from source to destination, e.g. '1 2 3 4'.")
        for q in range(10):
            print(f"[+] Challenge {q+1}/10.")
            while True:
                u, v = random.choices(list(G.nodes()), k=2)
                if u != v and nx.has_path(G, u, v):
                    break
            token = myGES.tokenGen(key, (u, v))
            print(f"[*] Token: {token.hex()}")
            tok, resp = myGES.search(token, enc_db)
            print(f"[*] Query Response: {tok.hex() + resp.hex()}")

            ans = input("> Original query: ").strip()
            if ans != decrypt(u, v, resp, key):
                print("[!] Wrong answer!")
                exit()
            if time.time() - t > 30:
                print("[!] Time's up!")
                exit()
        print(f"[+] Flag: {flag}")
    except:
        exit()
