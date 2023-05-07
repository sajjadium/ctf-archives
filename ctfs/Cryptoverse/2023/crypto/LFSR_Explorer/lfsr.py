from Crypto.Util.number import *
from secret import flag

assert flag.startswith("cvctf{")
assert flag.endswith("}")

flag = flag[6:-1].encode()
assert len(flag) == 8

def explore(state, mask):
    curr = (state << 1) & 0xffffffff
    i = state & mask & 0xffffffff
    last = 0
    while i != 0:
        last ^= (i & 1)
        i >>= 1
    curr ^= last
    return (curr, last)

states = [bytes_to_long(flag[4:]), bytes_to_long(flag[:4])]
mask = 0b10000100010010001000100000010101

output = []
for i in range(8):
    tmp = 0
    for j in range(8):
        (states[i // 4], out) = explore(states[i // 4], mask)
        tmp = (tmp << 1) ^ out
    output.append(tmp)

with open("output.txt", "wb") as f:
    f.write(bytes(output))
