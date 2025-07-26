from random import randint
from decimal import Decimal, getcontext
from hashlib import md5

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from secret import FLAG

K = randint(10**10, 10**11)
print('K', K)
leak = int( str( Decimal(K).sqrt() ).split('.')[-1] )

print(f"leak = {leak}")
ct = AES.new(
	md5(f"{K}".encode()).digest(),
	AES.MODE_ECB
).encrypt(pad(FLAG, 16))

print(f"ct = {ct.hex()}")
