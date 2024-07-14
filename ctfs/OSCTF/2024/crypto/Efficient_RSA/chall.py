from Cryptodome.Util.number import getPrime, bytes_to_long

Flag = bytes_to_long(b"REDACTED")

p = getPrime(112)
q = getPrime(112)
n = p*q
e = 65537

ciphertext = pow(Flag, e, n)

print([n, e, ciphertext])
