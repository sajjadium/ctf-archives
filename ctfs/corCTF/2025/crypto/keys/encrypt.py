from functools import reduce
import itertools
import os

def xor(x, y):
    return bytes([a ^ b for a, b in zip(x, y)])

def stream(keys0, keys1):
    for keys in itertools.product(*zip(keys0, keys1)):
        key = reduce(xor, keys)
        yield key

with open('flag.bmp', 'rb') as f:
    d = f.read()
    header = d[:len(d) - 1024 ** 2 * 3]
    data = d[len(d) - 1024 ** 2 * 3:]

keys0 = [os.urandom(3) for _ in range(20)]
keys1 = [os.urandom(3) for _ in range(20)]
ks = stream(keys0, keys1)

chunked = itertools.zip_longest(*[iter(data)] * 3)
encrypted = [
    xor(chunk, next(ks))
    for chunk in chunked
]

with open('flag-enc.bmp', 'wb') as f:
    f.write(header)
    f.write(b''.join(encrypted))

