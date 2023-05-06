from Crypto.Util.number import *
from secret import flag

p, q = getPrime(1333), getPrime(1333)
assert (p-1) % 1333 != 0 and (q-1) % 1333 != 0

mod = 1 << (3 * 333)
hint = (p % mod) ^ (q % mod)

enc = pow(bytes_to_long(flag), 1333, p * q)

print("N = {}".format(p * q))
print("hint = {}".format(hint))
print("enc = {}".format(enc))