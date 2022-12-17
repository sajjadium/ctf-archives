import random
import time
from Crypto.Util.number import bytes_to_long as b2l, long_to_bytes as l2b, getPrime

time.clock = time.time

# params
p = getPrime(2048)
q = getPrime(2048)
n = p*q
phi = (p-1)*(q-1)
e = 0x10001
d = pow(e, -1, phi)
print(f'e = {e}\nn = {n}')

# flag stuff
flag = open('flag.txt', 'r').read().strip()
assert(len(flag) == 38)
pts = [flag[0:len(flag)//2], flag[len(flag)//2:]]
#print(f'pts = {pts}\nl1 = {len(pts[0])} --- l2 = {len(pts[1])}')

# no more side channel attacks >:(
for i in range(2):
    pt = b2l(pts[i].encode())
    ct = pow(pt, e, n)

    rvals = [random.randrange(2, n-1) for _ in range(3)]
    ct2 = ct + rvals[0]*n
    d2 = d + rvals[1]*phi
    n2 = rvals[2]*n
    assert(pt == (pow(ct2, d2, n2) % n))

    print(f'ct_{i} = {ct}\nd2_{i} = {d2}\nrvals_{i} = {rvals}')


