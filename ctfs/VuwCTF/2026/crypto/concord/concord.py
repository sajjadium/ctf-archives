from random import seed, randbytes
from functools import reduce
import os

from Crypto.Cipher import AES

seed("concord")

def op(a,b):
    return (a+1)*(b+1)%257-1
rand_input = randbytes(2**30)
state = 0
key = []
for j in range(32):
    for i in range(1023):
        state = op(reduce(op, (op(rand_input[j+i], b) for b in rand_input)), state)
    key.append(state)

flag = os.environ.get("FLAG", "VuwCTF{xxxxxxxxxx}").encode(encoding="ascii")
cipher = AES.new(bytes(key), AES.MODE_CBC, iv=bytes.fromhex("243f57341528c28727458b8cc5f52786"))
print(cipher.encrypt(flag).hex())
