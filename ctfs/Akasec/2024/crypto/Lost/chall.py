from random import getrandbits
from Crypto.Util.number import getPrime, bytes_to_long
from SECRET import FLAG

e = 2
p = getPrime(256)
q = getPrime(256)
n = p * q

m = bytes_to_long(FLAG)
cor_m = m - getrandbits(160)

if __name__ == "__main__":
    c = pow(m, e, n)
    print("n = {}\nc = {}\ncor_m = {}".format(n, c, cor_m))
