from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from secrets import token_hex

p = 2**512 - 569
N = int(token_hex(64), 16)

fib1, fib2 = 0, 1
for _ in range(N - 1):
    fib1, fib2 = fib2, (fib1 + fib2) % p

key = SHA256.new(str(fib2).encode()).digest()
aes = AES.new(key, AES.MODE_CTR)

with open('../dev/flag.txt', 'r') as f:
    flag = bytes(f.readline(), 'ascii')

with open('task.txt', 'w') as f:
    f.write(aes.encrypt(flag).hex() + '\n')
    f.write(aes.nonce.hex() + '\n')
    f.write(hex(N)[2:])
