from secret import key
from hashlib import sha256


data = open("flag", "rb").read()

enc = b''

with open('a_space_odyssey.txt') as f:
    assert key.decode().lower() in f.read().lower()
    assert key.decode().isalnum()


HASH_ROUNDS = 1000000000

dat = key.lower()

for i in range(HASH_ROUNDS):
    dat = sha256(dat).digest()

dat = dat[:len(key)]

for a,b in zip(data,dat*(len(data))):
    enc += (a^b).to_bytes(1,'big')

with open("flag.enc","wb") as f:
    f.write(enc)