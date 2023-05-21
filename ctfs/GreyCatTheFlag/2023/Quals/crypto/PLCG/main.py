import secrets
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

FLAG = b'grey{fake_flag}'

while True:
    sample = [3, 80] + [secrets.randbelow(256) for _ in range(2)]
    if len(sample) == len(set(sample)) and 0 not in sample:
        break

def getBiasRandomByte():
    return secrets.choice(sample)

def getRandomByte():
    n = 0; g = 0
    for _ in range(20):
        n += getBiasRandomByte() * getBiasRandomByte()
    for _ in range(20):
        g = (g + getBiasRandomByte()) % 256 
    for _ in range(n):
        g = (getBiasRandomByte() * g + getBiasRandomByte()) % 256
    return g

def encrypt(msg):
    key = bytes([getRandomByte() for _ in range(6)])
    cipher = AES.new(pad(key, 16), AES.MODE_CTR, nonce=b'\xc1\xc7\xcc\xd1D\xfbI\x10')
    return cipher.encrypt(msg)

print("Hello there, this is our lucky numbers")
print(" ".join(map(str,sample)))

s = int(input("Send us your lucky number! "))

if not (0 <= s <= 10):
    print("I dont like your number :(")
    exit(0)

for i in range(s):
    print("Here's your lucky flag:", encrypt(FLAG).hex())
