from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import bytes_to_long,long_to_bytes
from secrets import generate_random_point_mod,small_noise
from os import urandom
n=bytes_to_long(urandom(16))
base,mod=generate_random_point_mod()
new_base=(base*n+small_noise())%mod
key=long_to_bytes(n)
flag=open("flag.txt","rb").read()
flag=pad(flag,16)
print("base=",base)
print("mod=",mod)
print("new_base=",new_base)
print("ciphertext="+AES.new(key,AES.MODE_ECB).encrypt(flag).hex())