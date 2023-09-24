import random
from secret import flag
def rc4():
    S = list(range(256))
    random.shuffle(S)
    i = random.randrange(256)
    j = random.randrange(256)
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        yield S[(S[i] + S[j]) % 256]
data = b'\x00'*1000 + flag
with open('data.bin','wb') as f:
    for i in range(200000):
        ciphertext = bytes([x^y for x,y in zip(data, rc4())])
        f.write(ciphertext)
