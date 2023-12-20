import random
import hashlib
from Crypto.Util.number import bytes_to_long
from Crypto.Cipher import AES

flag = b"The flag has been REDACTED"
secret = b"The seccret has been REDACTED"
key = hashlib.sha256(secret).digest()[:16]

cipher = AES.new(key, AES.MODE_ECB)
padded_flag = flag + b'\x00'*(-len(flag)%16)

ciphertext = cipher.encrypt(padded_flag)

f = open('output.txt','w')
f.write(f"Ciphertext: {ciphertext.hex()}\n\n")

arr = [ random.randint(1,1000000000000) for i in range(40) ]
k = bytes_to_long(secret)
s = 0
for i in range(40):
    if k&(1<<i):
        s+=arr[i]

f.write(f'numbers: {str(arr)[1:-1]}\nsum: {s}\n')
f.close()
