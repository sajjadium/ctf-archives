import random
from Crypto.Util.number import getPrime, bytes_to_long

flags = []

with open('stuff.txt', 'rb') as f:
    for stuff in f.readlines():
        flags.append(stuff)


with open('flag.txt', 'rb') as f:
    flag = f.read()
    flags.append(flag)

random.shuffle(flags)

for rand in flags:
    p = getPrime(1024)
    q = getPrime(1024)
    n = p * q
    e = 4
    m = bytes_to_long(rand)
    c = pow(m, e, n)
    with open('output.txt', 'a') as f:
        f.write(f'{n}\n')
        f.write(f'{e}\n')
        f.write(f'{c}\n\n')
    

