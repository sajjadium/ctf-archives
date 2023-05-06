import random
from Crypto.Cipher import AES

# generate key
gpList = [ [13, 19], [7, 17], [3, 31], [13, 19], [17, 23], [2, 29] ]
g, p = random.choice(gpList)
a = random.randint(1, p)
b = random.randint(1, p)
k = pow(g, a * b, p)
k = str(k)

# print("Diffie-Hellman key exchange outputs")
# print("Public key: ", g, p)
# print("Jotaro sends: ", aNum)
# print("Dio sends: ", bNum)
# print()

# pad key to 16 bytes (128bit)
key = ""
i = 0
padding = "uiuctf2021uiuctf2021"
while (16 - len(key) != len(k)):
    key = key + padding[i]
    i += 1
key = key + k
key = bytes(key, encoding='ascii')

with open('flag.txt', 'rb') as f:
    flag = f.read()

iv = bytes("kono DIO daaaaaa", encoding = 'ascii')
cipher = AES.new(key, AES.MODE_CFB, iv)
ciphertext = cipher.encrypt(flag)

print(ciphertext.hex())
