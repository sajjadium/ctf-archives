#!/usr/local/bin/python

from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
from random import randint
from binascii import hexlify

with open('flag.txt','r') as f:
    flag = f.read().strip()

with open('keyfile','rb') as f:
    key = f.read()
    assert len(key)==32

'''
Pseudorandom number generators are weak!
True randomness comes from phyisical objects, like dice!
'''
class TrueRNG:

    @staticmethod
    def die():
        return randint(1, 6)

    @staticmethod
    def yahtzee(N):
        dice = [TrueRNG.die() for n in range(N)]
        return sum(dice)

    def __init__(self, num_dice):
        self.rolls = num_dice

    def next(self):
        return TrueRNG.yahtzee(self.rolls)

def encrypt(message, key, true_rng):
    nonce = true_rng.next()
    cipher = AES.new(key, AES.MODE_CTR, nonce = long_to_bytes(nonce))
    return cipher.encrypt(message)

'''
Stick the flag in a random quote!
'''
def random_message():
    NUM_QUOTES = 25
    quote_idx = randint(0,NUM_QUOTES-1)
    with open('quotes.txt','r') as f:
        for idx, line in enumerate(f):
            if idx == quote_idx:
                quote = line.strip().split()
                break
    quote.insert(randint(0, len(quote)), flag)
    return ' '.join(quote)

banner = '''
============================================================================
=            Welcome to the yahtzee message encryption service.            =
=  We use top-of-the-line TRUE random number generators... dice in a cup!  =
============================================================================
Would you like some samples?
'''
prompt = "Would you like some more samples, or are you ready to 'quit'?\n"

if __name__ == '__main__':
    NUM_DICE = 2
    true_rng = TrueRNG(NUM_DICE)
    inp      = input(banner)
    while 'quit' not in inp.lower():
        message = random_message().encode()
        encrypted = encrypt(message, key, true_rng)
        print('Ciphertext:', hexlify(encrypted).decode())
        inp = input(prompt)
