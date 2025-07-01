from Crypto.Util.number import getPrime, bytes_to_long
flag = "grodno{REDACTED}"

p = getPrime(1024)
q = getPrime(1024)
n = p * q

e = 65537
c = pow(bytes_to_long(flag.encode()), e, n)

xor = p ^ int(bin(q)[2:][::-1], 2)

print(f"RSA module (n): {n}")
print(f"Ciphertext (c): {c}")
print(f"XOR: {xor}")