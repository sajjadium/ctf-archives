from Cryptodome.Util.number import long_to_bytes, getPrime, bytes_to_long

m = b"Blitz{REDACTED}"

p = getPrime(150)
q = getPrime(150)
e = getPrime(128)
n = p*q
mod_phi = (p-1)*(q-1)*(e-1)
d = pow(e, -1, mod_phi)

print(mod_phi)
print(n)
c = pow(bytes_to_long(m), e, n)
print(c)
