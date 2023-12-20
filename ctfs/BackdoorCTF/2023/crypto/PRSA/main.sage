from sage.all import *
from Crypto.Util.number import bytes_to_long, getPrime

import random
import time
random.seed(time.time())

message = b'flag{REDACTED}' ## the flag has been removed
F.<x> = PolynomialRing(GF(2), x)

p, q = [F.irreducible_element(random.randint(2 ** 10, 2 ** 12)) for _ in range(2)]
R.<y> = F.quotient_ring(p * q)

n = sum(int(bit) * y ** (len(bin(bytes_to_long(message))[2:]) - 1 - i) for i, bit in enumerate(bin(bytes_to_long(message))[2:]))

e = 2 ** 256
c = n ** e 

print(e) ## to be given to the user
print(c) ## to be given to the user
print(p * q) ## to be given to the user

