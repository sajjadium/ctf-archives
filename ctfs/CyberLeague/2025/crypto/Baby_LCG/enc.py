from Crypto.Cipher import AES
from Crypto.Random.random import getrandbits
from Crypto.Util.number import getPrime, long_to_bytes
from Crypto.Util.Padding import pad
import binascii

while True:
    key = getrandbits(128)
    mult = getrandbits(128)
    inc = getrandbits(128)
    mod = getPrime(128)
    if key < mod and mult < mod and inc < mod:
        break

flag = b"[REDACTED]"
cipher = AES.new(long_to_bytes(key), AES.MODE_CBC)
ct = cipher.encrypt(pad(flag, AES.block_size))

print("ct =", binascii.hexlify(ct))
print("iv =", binascii.hexlify(cipher.iv))
print("mod =", mod)

for i in range(1, 58):
    key = (key * mult + inc) % mod
    if i % 19 == 0:
        print("Round", i, "-", key)