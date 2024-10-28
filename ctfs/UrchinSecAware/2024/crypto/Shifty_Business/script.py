from functools import reduce

def ecv(v):

    n = [16, 32, 64, 128]
    return reduce(lambda v, s: (v << s) ^ s, n, v)

flag = "urchinsec{xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx}"
enc = [ecv(ord(char) ** 2) for char in flag]

print(enc)
