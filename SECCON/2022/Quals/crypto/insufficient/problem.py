from random import randint
from Crypto.Util.number import getPrime, bytes_to_long
from secret import FLAG


# f(x,y,z) = a1*x + a2*x^2 + a3*x^3
#          + b1*y + b2*y^2 + b3*y^3
#          + c*z + s mod p
def calc_f(coeffs, x, y, z, p):
    ret = 0
    ret += x * coeffs[0] + pow(x, 2, p) * coeffs[1] + pow(x, 3, p)*coeffs[2]
    ret += y * coeffs[3] + pow(y, 2, p) * coeffs[4] + pow(y, 3, p)*coeffs[5]
    ret += z * coeffs[6]
    ret += coeffs[7]

    return ret % p


p = getPrime(512)


# [a1, a2, a3, b1, b2, b3, c, s]
coeffs = [randint(0, 2**128) for _ in range(8)]

key = 0
for coeff in coeffs:
    key <<= 128
    key ^= coeff

cipher_text = bytes_to_long(FLAG) ^ key
print(cipher_text)

shares = []
for _ in range(4):
    x = randint(0, p)
    y = randint(0, p)
    z = randint(0, 2**128)

    w = calc_f(coeffs, x, y, z, p)
    packed_share = ((x,y), w)
    shares.append(packed_share)

print(p)
print(shares)