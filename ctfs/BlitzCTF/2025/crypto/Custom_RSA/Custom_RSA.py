from Cryptodome.Util.number import getPrime, bytes_to_long

m = b"Blitz{REDACTED}"

p = getPrime(256)
q = getPrime(256)
x = getPrime(128)
y = getPrime(128)
z = getPrime(128)
e = x*y*z
n = p*q*y
hint1 = p % x
hint2 = p % z

print("hint1 = ", hint1)
print("hint2 = ", hint2)
print("n = ", n)
print("e = ", e)
c = pow(bytes_to_long(m), e, n)
print("c = ", c)
