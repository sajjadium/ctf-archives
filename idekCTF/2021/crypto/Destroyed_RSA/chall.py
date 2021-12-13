import random
from Crypto.Util.number import bytes_to_long, getPrime, isPrime
from flag import flag

f = flag

def interesting_prime():
    #recognize me?
    D = 987
    while True:
        s = random.randint(2**1020,2**1021-1)
        check = D * s ** 2 + 1
        if check % 4 == 0 and isPrime((check // 4)):
            return check // 4


m = bytes_to_long(f)
p = interesting_prime()
q = getPrime(2048)
N = p*q
e = 6551
c = pow(m, e, N)

with open('out.txt', 'w') as w:
    w.write(f"n = {N}")
    w.write(f"e = {e}")
    w.write(f"c = {c}")