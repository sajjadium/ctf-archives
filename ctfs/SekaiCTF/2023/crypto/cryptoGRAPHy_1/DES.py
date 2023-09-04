from __future__ import annotations
from typing import *
from Crypto.Random import get_random_bytes
from itertools import product
from multiprocessing import Pool
import utils

class DESClass:
    '''
    Implementation of dictionary encryption scheme
    '''
    def __init__(self, encrypted_db: dict[bytes, bytes] = {}):
        self.encrypted_db = encrypted_db

    def keyGen(self, security_parameter: int) -> bytes:
        '''
        Input: Security parameter
        Output: Secret key
        '''
        return get_random_bytes(security_parameter)

    def encryptDict(self, key: bytes, plaintext_dx: dict[bytes, bytes], cores: int) -> dict[bytes, bytes]:
        '''
        Input: A key and a plaintext dictionary
        Output: An encrypted dictionary EDX
        '''
        encrypted_db = {}
        chunk = int(len(plaintext_dx)/cores)
        iterable = product([key], plaintext_dx.items())

        with Pool(cores) as pool:
            for ct_label, ct_value in pool.istarmap(encryptDictHelper, iterable, chunksize=chunk):   
                encrypted_db[ct_label] = ct_value
        return encrypted_db

    def tokenGen(self, key: bytes, label: bytes) -> bytes:
        '''
        Input: A key and a label
        Output: A token on label
        '''
        K1 = utils.HashMAC(key, b'1'+label)[:16]
        K2 = utils.HashMAC(key, b'2'+label)[:16]
        return K1 + K2

    def search(self, search_token: bytes, encrypted_db: dict[bytes, bytes]) -> bytes:
        '''
        Input: Search token and EDX
        Output: The corresponding encrypted value.
        '''
        K1 = search_token[:16]
        K2 = search_token[16:]
        hash_val = utils.Hash(K1)
        if hash_val in encrypted_db:
            ct_value = encrypted_db[hash_val]
            return utils.SymmetricDecrypt(K2, ct_value)
        else:
            return b''

def encryptDictHelper(key, dict_item):
    label = dict_item[0]
    value = dict_item[1]

    K1 = utils.HashMAC(key, b'1'+label)[:16]
    K2 = utils.HashMAC(key, b'2'+label)[:16]

    ct_label = utils.Hash(K1)
    ct_value = utils.SymmetricEncrypt(K2, value)
    return ct_label, ct_value