from Cryptodome.Util.number import getPrime, bytes_to_long

flag = bytes_to_long(b"REDACTED")
p = getPrime(512)
q = getPrime(512)
n = p*q
e = 3

ciphertext = pow(flag, e, n)

print("n: ", n)
print("e: ", e)
print("ciphertext: ", ciphertext)

