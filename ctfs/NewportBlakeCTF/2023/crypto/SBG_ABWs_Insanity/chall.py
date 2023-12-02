from Crypto.Util.number import getPrime, bytes_to_long, isPrime, long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hashlib

m = bytes_to_long(b'we give you this as a gift!')

p = getPrime(1096)
q1 = getPrime(1096)
q2 = getPrime(1096)
n1 = p*q1
n2 = p*q2

e = 11

ct1 = pow(m,e,n1)
ct2 = pow(m,e,n2)

key = hashlib.sha256(long_to_bytes(q1)).digest()
cipher = AES.new(key, AES.MODE_ECB)
enc_flag = cipher.encrypt(pad(b"nbctf{[REDACTED]}", 16))

print("ct1 =", ct1)
print("ct2 =", ct2)
print("enc_flag =", enc_flag.hex())