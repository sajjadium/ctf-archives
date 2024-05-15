from Crypto.Util.number import getPrime, isPrime, long_to_bytes
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from hashlib import sha256

with open('flag.txt', 'rb') as rf:
    flag = rf.read().strip()

path = "lazydh.txt"

p = getPrime(160)
q = (p-1)//2
while not isPrime(q):
    p = getPrime(160)
    q = (p-1)//2

g = 2
while pow(g, q, p) != 1:
    g += 1

with open("secret_a_b.txt") as rf:
    a = int(rf.readline())
    b = int(rf.readline())

assert a.bit_length() == b.bit_length() == 128

a_digits = [int(d) for d in str(a)]

ga = pow(g, a, p)
gb = pow(g, b, p)
shared = pow(ga, b, p)

a1_digits = [(d + 1) % 10 for d in a_digits]
a1 = int(''.join(map(str, a1_digits)))

new_shared = pow(gb, a1, p)

key = sha256(long_to_bytes(new_shared)).digest()
cipher = AES.new(key, AES.MODE_ECB)
enc_flag = cipher.encrypt(pad(flag.encode(), AES.block_size)).hex()

with open(path, 'w') as wf:
    wf.write(f"{p = }\n")
    wf.write(f"{ga = }\n")
    wf.write(f"{gb = }\n")
    wf.write(f"{shared = }\n")
    wf.write(f"{enc_flag = }\n")