import random
from secret import FLAG

assert FLAG.startswith('n1ctf{')
assert FLAG.endswith('}')
SECRET = bytes.fromhex(FLAG[6:-1])
assert len(SECRET) == 16

p = 251
 
e = [1, 20, 113, 149, 219]

y = b'' 
for x in range(1, p):
    coeff = [random.choice(e)] + list(SECRET)
    y += bytes([sum(c * pow(x, i, p) for i, c in enumerate(coeff)) % p])
    
print(f'Token: {y.hex()}')
