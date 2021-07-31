from random import randint
from Crypto.Util.number import isPrime
from Crypto.Cipher import AES
from hashlib import sha256

print("I'm too lazy to find parameters for my DHKE, choose for me.")
print("Enter prime at least 1024 at most 2048 bits: ")
# get user's choice of p
p = input()
p = int(p)
# check prime valid
if p.bit_length() < 1024 or p.bit_length() > 2048 or not isPrime(p):
    exit("Invalid input.")
# prepare for key exchange
g = 2
a = randint(2,p-1)
b = randint(2,p-1)
# generate key
dio = pow(g,a,p)
jotaro = pow(g,b,p)
key = pow(dio,b,p)
key = sha256(str(key).encode()).digest()

with open('flag.txt', 'rb') as f:
    flag = f.read()

iv = b'uiuctf2021uiuctf'
cipher = AES.new(key, AES.MODE_CFB, iv)
ciphertext = cipher.encrypt(flag)

print("Dio sends: ", dio)
print("Jotaro sends: ", jotaro)
print("Ciphertext: ", ciphertext.hex())
