import hashlib
from icecream import *
from private_data import keys,flag
from Crypto.Util.number import *



def xor(A, B):
    return bytes(a ^ b for a, b in zip(A, B))
the_chaos=b''

for i in keys:
    tmp = sum(keys[i])
    the_chaos += bytes(long_to_bytes(tmp))
mask = hashlib.md5(the_chaos).digest()
print(xor(mask,flag).hex())

# 1661fe85c7b01b3db1d432ad3c5ac83a