from os import urandom
import binascii
import time

flag = r'flag{fake_flag}'

######### Public
m = int(binascii.hexlify(urandom(16)), 16)

######### Secret
a = int(binascii.hexlify(urandom(4)), 16) % m
b = int(binascii.hexlify(urandom(4)), 16) % m

######### Encrypt
otp = []
otp.append(int(time.time()) % m)

for _ in range(50):
    next = (a * otp[-1] + b) % m
    otp.append(next)

enc = ""
for i in range(len(flag)):
    enc += str(ord(flag[i]) ^ otp[i+1]) + " "

print("######### Output #########")
print("m ", m)
print("enc ", enc)
print("######### End #########")