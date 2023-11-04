# See also https://github.com/tsg-ut/pycryptodome
from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
from Crypto.Util.number import getPrime
from Crypto.Random.random import randrange
from base64 import b64decode
from signal import alarm
import os

alarm(15)

q = getPrime(256)
print(f'q = {q}')

p = int(input('p? '))
h = int(input('h? '))

g = pow(h, (p - 1) // q, p)
x = randrange(q)
y = pow(g, x, p)

print(f'g = {g}')
print(f'y = {y}')

dsa = DSA.construct((y, g, p, q, x))
dss = DSS.new(dsa, 'fips-186-3')

print('Thank you for helping me with DSA! Now give me the base64-encoded signature of sha256("flag")')
sign = b64decode(input('sign? '))

dss.verify(SHA256.new(b'flag'), sign)
print(f"Awesome! {os.environ.get('FLAG')}")
