from Crypto.Util.number import *
from Crypto.PublicKey import RSA

e = 65537
flag = b'ACTF{...}'

while True:
    p = getPrime(1024)
    q = inverse(e, p)
    if not isPrime(q):
        continue
    n = p * q;
    public = RSA.construct((n, e))
    with open("public.pem", "wb") as file:
        file.write(public.exportKey('PEM'))
    with open("flag", "wb") as file:
        file.write(long_to_bytes(pow(bytes_to_long(flag), e, n)))
    break
