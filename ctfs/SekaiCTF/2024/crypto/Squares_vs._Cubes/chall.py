from Crypto.Util.number import bytes_to_long, getPrime
from secrets import token_bytes, randbelow
from flag import FLAG

padded_flag = bytes_to_long(FLAG + token_bytes(128 - len(FLAG)))

p, q, r = getPrime(512), getPrime(512), getPrime(512)
N = e = p * q * r
phi = (p - 1) * (q - 1) * (r - 1)
d = pow(e, -1, phi)

# Genni likes squares and SBG likes cubes. Let's calculate their values
value_for_genni = p**2 + (q + r * padded_flag)**2
value_for_sbg   = p**3 + (q + r * padded_flag)**3

x0 = randbelow(N)
x1 = randbelow(N)

print(f'{N = }')
print(f'{x0 = }')
print(f'{x1 = }')
print('\nDo you prefer squares or cubes? Choose wisely!')

# Generate a random k and send v := (x_i + k^e), for Oblivious Transfer
# This will allow you to calculate either Genni's or SBG's value
# I have no way of knowing who you support. Your secret is completely safe!
v = int(input('Send me v: '))

m0 = (pow(v - x0, d, N) + value_for_genni) % N
m1 = (pow(v - x1, d, N) + value_for_sbg) % N
print(f'{m0 = }')
print(f'{m1 = }')