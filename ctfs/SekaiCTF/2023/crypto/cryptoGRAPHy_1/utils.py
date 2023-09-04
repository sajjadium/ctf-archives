from typing import *
import multiprocessing.pool as mpp
import networkx as nx
from Crypto.Hash import HMAC, SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

'''
Utility functions
'''
def istarmap(self, func, iterable, chunksize):
    '''
    starmap equivalent using imap.
    Feel free to ignore this function for challenge purposes.
    '''
    if self._state != mpp.RUN:
        raise ValueError("Pool not running")
    if chunksize < 1:
        raise ValueError("Chunksize must be 1+, not {0:n}".format(chunksize))

    task_batches = mpp.Pool._get_tasks(func, iterable, chunksize)
    result = mpp.IMapIterator(self)
    self._taskqueue.put((
        self._guarded_task_generation(result._job, mpp.starmapstar, task_batches),
        result._set_length
    ))
    return (item for chunk in result for item in chunk)

mpp.Pool.istarmap = istarmap

def int_to_bytes(x: int) -> bytes:
    return str(x).encode()

def pair_to_bytes(pair: Tuple[int, int]) -> bytes:
    return int_to_bytes(pair[0]) + b',' + int_to_bytes(pair[1])

def generate_graph(edges: List[List[int]]) -> nx.Graph:
    '''
    Input: A list of edges (u, v)
    Output: A networkx graph
    '''
    G = nx.Graph()
    for edge in edges:
        G.add_edge(*edge)
    return G

def Hash(data: bytes) -> bytes:
    h = SHA256.new()
    h.update(data)
    return h.digest()

def SymmetricEncrypt(key: bytes, plaintext: bytes) -> bytes:
    '''
    Encrypt the plaintext using AES-CBC mode with provided key.
    Input: 16-byte key and plaintext
    Output: Ciphertext
    '''
    if len(key) != 16:
        raise ValueError

    cipher = AES.new(key, AES.MODE_CBC)
    ct = cipher.encrypt(pad(plaintext, AES.block_size))
    iv = cipher.iv
    return ct + iv

def SymmetricDecrypt(key: bytes, ciphertext: bytes) -> bytes:
    '''
    Decrypt the ciphertex using AES-CBC mode with provided key.
    Input: 16-byte key and ciphertext
    Output: Plaintext
    '''
    if len(key) != 16:
        raise ValueError

    ct, iv = ciphertext[:-16], ciphertext[-16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt

def HashMAC(key: bytes, plaintext: bytes) -> bytes:
    '''
    Input: Key and plaintext
    Output: A token on plaintext with the key using HMAC
    '''
    token = HMAC.new(key, digestmod=SHA256)
    token.update(bytes(plaintext))
    return token.digest()


if __name__ == '__main__':
    # Test SymmetricEncrypt and SymmetricDecrypt
    key = b"a" * 16
    plaintext = b"Hello world!"
    ciphertext = SymmetricEncrypt(key, plaintext)
    assert SymmetricDecrypt(key, ciphertext) == plaintext

    # Test generate_graph
    G = generate_graph([[1, 2], [2, 4], [1, 3], [3, 5], [5, 4]])
    assert G.number_of_nodes() == 5
    assert nx.shortest_path(G, 1, 4) == [1, 2, 4]