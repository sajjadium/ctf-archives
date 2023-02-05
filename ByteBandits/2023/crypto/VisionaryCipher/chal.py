from string import ascii_lowercase, digits
from random import choices
from hashlib import md5

with open("flag.txt", "r") as f:
    FLAG = f.read()

alphabets = ascii_lowercase + digits + "_{}"
key = "".join(choices(alphabets, k=10))


def pos(ch):
    return alphabets.find(ch)


def encrypt(text, key):
    k, n, l = len(key), len(text), len(alphabets)
    return "".join([alphabets[(pos(text[i]) + pos(key[i % k])) % l] for i in range(n)])


print("c :", encrypt(FLAG, key))
print("hash :", md5(FLAG.encode("ascii")).hexdigest())