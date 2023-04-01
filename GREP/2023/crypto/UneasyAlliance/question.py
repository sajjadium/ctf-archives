from Crypto.Util.number import *
import math
import time
from random import Random

seed = math.floor(time.time())
rnd = Random(seed)

rand_fn = lambda n: long_to_bytes(rnd.getrandbits(n))
p = getPrime(128, randfunc=rand_fn)
q = getPrime(128, randfunc=rand_fn)
e = 65537
n = p * q

assert p != q

m = bytes_to_long(b"GREP{REDACTED}")
ct = pow(m, e, n)
print("Cipher text:", ct)
# Cipher text: 9898717456951148133749957106576029659879736707349710770560950848503614119828
# Seed: REDACTED