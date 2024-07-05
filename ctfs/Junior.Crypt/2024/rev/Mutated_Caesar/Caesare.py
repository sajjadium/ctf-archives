from random import randint
from hashlib import md5
from secret import flag

hash = md5(flag.encode()).hexdigest()

n1, n2 = randint(0x20, 0x41), randint(0x7d, 0x7e)
CN = {chr(i+n1): i for i in range(0, n2-n1+1)}
NC = {i: chr(i+n1) for i in range(0, n2-n1+1)}

N = len(CN.keys())
key = randint(0,N)

cipher = "".join([NC[(CN[c] + key) % N] for c in flag])

print (f"cipher = {cipher}")
print (f"md5 = {hash}")