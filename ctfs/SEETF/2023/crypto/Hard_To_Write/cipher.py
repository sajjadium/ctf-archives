import numpy as np
from _cipher import *

def decrypt(pt:bytes, key:int) -> bytes:
    return internal_decrypt(np.frombuffer(pt, dtype=np.uint8), key).tobytes()

def encrypt(pt:bytes, key:int) -> bytes:
    return internal_encrypt(np.frombuffer(pt, dtype=np.uint8), key).tobytes()