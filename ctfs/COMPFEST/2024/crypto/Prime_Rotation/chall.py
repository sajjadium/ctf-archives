from sage.all import *
from Crypto.Util.number import *

flag = b'COMPFEST16{REDACTED}'

while True:
    p = next_prime(randrange(10*299, 10**300))
    if len(str(p)) != 300:
        continue
    q = Integer(int(str(p)[200:] + str(p)[100:200] + str(p)[:100]))
    if is_prime(q):
        if len(str(p*q)) == 600:
            n = p*q
            ct = pow(bytes_to_long(flag), 65537, n)
            print("ct =", ct)
            print("n =", n)
            break
