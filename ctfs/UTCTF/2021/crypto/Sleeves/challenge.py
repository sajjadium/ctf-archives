from challenge.eccrng import RNG
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

rng = RNG()
# I'll just test it out a few times first
print("r1 = %d" % rng.next())
print("r2 = %d" % rng.next())

r = str(rng.next())
aes_key = SHA256.new(r.encode('ascii')).digest()
cipher = AES.new(aes_key, AES.MODE_ECB)
print("ct = %s" % cipher.encrypt(b"????????????????????????????????????????").hex())

