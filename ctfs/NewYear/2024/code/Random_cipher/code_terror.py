from random import randint

def encrypt(text):
    key = randint(1, 2 * len(text))
    print (ord(text[0]), key)
    result = []

    for c in text:
        result.append(ord(c) + (ord(c) % key))
        key = key + 1

    return result