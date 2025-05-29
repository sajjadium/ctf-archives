from Crypto.Util.number import getStrongPrime, inverse, GCD, bytes_to_long
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import random
import hashlib
import os

FLAG = b"[REDACTED]"

e = 0x10001
while True:
    p = getStrongPrime(2048)
    q = getStrongPrime(2048)
    phi = (p-1)*(q-1)
    d = inverse(e, phi)
    if d > 1 and GCD(e, phi) == 1:
        break

N = p * q
ct = pow(bytes_to_long(FLAG),e,N)

print(N)
print(e)
print(ct)

d2 = bin(d)[2:][::-1]
d2 = bin(int(d2,2) ^ d)[-1600:]
d2_blocs = [d2[k*1600//8:(k+1)*1600//8] for k in range(8)]
d2_mixed_up = [None] * 8
mix_order = ""
while None in d2_mixed_up :
    r = random.randint(0,7)
    if d2_mixed_up[r] :
        r = random.randint(0,7)
    if not d2_mixed_up[r] :
        d2_mixed_up[r] = d2_blocs.pop()
    mix_order += '-'+str(r) if mix_order else str(r)
d2_mixed_up = "".join(d2_mixed_up)

derived_aes_key = hashlib.sha256(mix_order.encode('ascii')).digest()
iv = os.urandom(16)
cipher = AES.new(derived_aes_key, AES.MODE_CBC, iv)
d2_mixed_up_encrypted = cipher.encrypt(pad(int(d2_mixed_up,2).to_bytes((len(d2_mixed_up)+7)//8,'big'),16,'pkcs7'))

mix_protection_hash = hashlib.md5()
mix_protection_hash.update(mix_order.encode('ascii'))

print("{}:{}".format(iv.hex(), d2_mixed_up_encrypted.hex()))
print("{}:{}".format(len(mix_order)//2+1, mix_protection_hash.hexdigest()))
