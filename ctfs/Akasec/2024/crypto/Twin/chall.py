from Crypto.Util.number import getPrime, bytes_to_long
from SECRET import FLAG

e = 5
p = getPrime(256)
q = getPrime(256)
n = p * q

m1 = bytes_to_long(FLAG)
m2 = m1 >> 8

if __name__ == "__main__":
    c1, c2 = pow(m1, e, n), pow(m2, e, n)
    print("n = {}\nc1 = {}\nc2 = {}".format(n, c1, c2))