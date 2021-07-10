import random

key = random.randint(0, 25)
alphabet = 'abcdefghijklmnopqrstuvwxyz'
shifted = alphabet[key:] + alphabet[:key]
dictionary = dict(zip(alphabet, shifted))

print(''.join([
    dictionary[c]
    if c in dictionary
    else c
    for c in input()
]))
