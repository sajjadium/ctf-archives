import os
from secret import KEY
assert len(KEY) == 2
assert KEY[1] == 64

def crypt(n):
    m = (1<<KEY[1])-1
    iv = os.urandom(KEY[1]//8)
    x = int.from_bytes(iv, 'big') & m
    y = bytearray()
    for _ in range(n):
        b = 0
        for i in range(8):
            b += (x&1)
            if i!=7: b <<= 1
            f = sum(((x>>p)&1) for p in KEY[0])&1
            x = ((x>>1)|(f<<(KEY[1]-1))) & m
        y.append(b)
    return bytes(y)


with open("db.db", "rb") as f:
    data = f.read()

with open("db.enc", "wb") as f:
    f.write(bytes(a^b for a,b in zip(data, crypt(len(data)))))