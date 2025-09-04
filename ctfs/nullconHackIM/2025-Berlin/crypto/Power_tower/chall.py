from Crypto.Cipher import AES
from Crypto.Util import number

# n = number.getRandomNBitInteger(256)
n = 107502945843251244337535082460697583639357473016005252008262865481138355040617

primes = [p for p in range(100) if number.isPrime(p)]
int_key = 1
for p in primes: int_key = p**int_key

key = int.to_bytes(int_key % n,32, byteorder = 'big')

flag = open('flag.txt','r').read().strip()
flag += '_' * (-len(flag) % 16)
cipher = AES.new(key, AES.MODE_ECB).encrypt(flag.encode())
print(cipher.hex())
