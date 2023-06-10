from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
from Crypto.Hash import SHA256
import random, string, binascii, re
p = getPrime(2048)
q = getPrime(2048)
n = p*q
e = 3
chars = string.digits + string.ascii_letters + string.punctuation
t = "".join(random.sample(chars, 20))
h = SHA256.new()
h.update(bytes(t, 'utf-8'))
print(f'n = {n}')
print(f'Provide a signature for the text {t}')
try:
    sig = bytes_to_long(binascii.unhexlify(input(": ")))
    str = long_to_bytes(pow(sig, e, n))
    hash = re.findall(rb'\x01\xff*\x00(.{32})', str)[0] # PKCS padding
    if hash == h.digest():
        with open("flag.txt", "r") as f:
            print(f.read())
    else:
        print("Incorrect")
except:
    print("Incorrect")
