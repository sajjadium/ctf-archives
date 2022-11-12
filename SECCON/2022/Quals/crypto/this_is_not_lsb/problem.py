from Crypto.Util.number import *
from flag import flag

p = getStrongPrime(512)
q = getStrongPrime(512)
e = 65537
n = p * q
phi = (p - 1) * (q - 1)

d = pow(e, -1, phi)

print(f"n = {n}")
print(f"e = {e}")
print(f"flag_length = {flag.bit_length()}")

# Oops! encrypt without padding!
c = pow(flag, e, n)
print(f"c = {c}")

# padding format: 0b0011111111........
def check_padding(c):
    padding_pos = n.bit_length() - 2
    m = pow(c, d, n)

    return (m >> (padding_pos - 8)) == 0xFF


while True:
    c = int(input("c = "))
    print(check_padding(c))
