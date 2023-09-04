from __future__ import annotations
from typing import *
from multiprocessing import Pool
from itertools import product
from Crypto.Random import get_random_bytes

import networkx as nx
import gc
import DES
import utils

DES = DES.DESClass({})

class GESClass:
    '''
    Implementation of graph encryption scheme
    '''
    def __init__(self, cores: int, encrypted_db: dict[bytes, bytes] = {}):
        self.encrypted_db = encrypted_db
        self.cores = cores

    def keyGen(self, security_parameter: int) -> bytes:
        '''
        Input: Security parameter
        Output: Secret key key_SKE||key_DES
        '''
        key_SKE = get_random_bytes(security_parameter)
        key_DES = DES.keyGen(security_parameter)
        return key_SKE + key_DES

    def encryptGraph(self, key: bytes, G: nx.Graph) -> dict[bytes, bytes]:
        '''
        Input: Secret key and a graph G
        Output: Encrypted graph encrypted_db
        '''
        SPDX = computeSPDX(key, G, self.cores)

        key_DES = key[16:]    
        EDB = DES.encryptDict(key_DES, SPDX, self.cores)

        del(SPDX)
        gc.collect()

        return EDB
    
    def tokenGen(self, key: bytes, query: tuple(int,int)) -> bytes:
        key_DES = key[16:]
        label = utils.pair_to_bytes(query)
        return DES.tokenGen(key_DES, label)
        
    def search(self, token: bytes, encrypted_db: dict[bytes, bytes]) -> Tuple(bytes, bytes):
        '''
        Input: Search token
        Output: (tokens, cts)
        '''
        resp, tok = b"", b""
        curr = token

        while True:
            value = DES.search(curr, encrypted_db)
            if value == b'':
                break
            curr = value[:32]
            resp += value[32:]
            tok += curr
        return tuple([tok, resp])

def computeSDSP(G: nx.Graph, root):
    '''
    Input: Graph G and a root
    Output: Tuples of the form ((start, root), (next_vertex, root))
    '''
    paths = nx.single_source_shortest_path(G, root)

    S = set()
    for _, path in paths.items():   
        path.reverse()
        if len(path) > 1:
            for i in range(len(path)-1):
                label = (path[i], root)
                value = (path[i+1],root)
                S.add((label, value))
    return S

def computeSPDX(key: bytes, G: nx.Graph, cores: int) -> dict[bytes, bytes]:
    SPDX = {}
    chunk = round(len(G.nodes())/cores)
    
    key_SKE = key[:16]
    key_DES = key[16:]
    
    with Pool(cores) as pool:
        iterable = product([G], G)
        
        for S in pool.istarmap(computeSDSP, iterable, chunksize=chunk):
            for pair in S:
                label, value = pair[0], pair[1]
                label_bytes = utils.pair_to_bytes(label)
                value_bytes = utils.pair_to_bytes(value)

                if label_bytes not in SPDX:
                    token = DES.tokenGen(key_DES, value_bytes)
                    ct = utils.SymmetricEncrypt(key_SKE,value_bytes)
                    ct_value = token + ct
                    SPDX[label_bytes] = ct_value
    return SPDX