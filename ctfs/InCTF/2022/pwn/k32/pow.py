import hashlib

def solvepow(x, target):
    x = bytes.fromhex(x)
    target = bytes.fromhex(target)
    for i in range(256**3):
        if hashlib.md5(x + i.to_bytes(3, "big")).digest() == target:
            return x.hex()+hex(i)[2:]