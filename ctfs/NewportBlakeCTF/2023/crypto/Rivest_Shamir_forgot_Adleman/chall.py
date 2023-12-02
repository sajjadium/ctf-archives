from Crypto.Util.number import *

p = getPrime(1024)
q = getPrime(1024)

n = p*q
e = 123589168751396275896312856328164328381265978316578963271231567137825613822284638216416
m = bytes_to_long(b"nbctf{[REDACTED]}")

ct = (m^e) % n

print("n = ", n)
print("e = ", e)
print("ct = ", ct)