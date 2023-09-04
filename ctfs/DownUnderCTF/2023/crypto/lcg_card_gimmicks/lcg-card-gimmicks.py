#!/usr/bin/env python3

from secrets import randbelow
import signal


DECK = [f'{val}{suit}' for suit in 'CDHS' for val in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']] + ['RJ', 'BJ']
M = 2**64


class LCG:
    def __init__(self, seed, A=None, C=None):
        self.M = M
        if A is None:
            self.A = randbelow(self.M) | 1
        else:
            self.A = A
        if C is None:
            self.C = randbelow(self.M)
        else:
            self.C = C
        self.seed = seed

    def __str__(self):
        o = f'A = {self.A}\n'
        o += f'C = {self.C}\n'
        o += f'M = {self.M}'
        return o

    def next(self):
        self.seed = (self.A * self.seed + self.C) % self.M
        return self.seed

    def between(self, lo, hi):
        r = self.next()
        return lo + (r >> 16) % (hi - lo)


def draw(rng, k):
    hand = []
    while len(hand) < k:
        r = rng.between(0, len(DECK)) 
        card = DECK[r]
        if card in hand:
            continue
        hand.append(card)
    return hand


def main():
    seed = randbelow(M)
    rng = LCG(seed)
    print(rng)

    hand = draw(rng, 13)
    print('My hand:', ' '.join(hand))

    guess = int(input('Show me a magic trick: '))
    if hand == draw(LCG(guess, A=rng.A, C=rng.C), 13):
        FLAG = open('flag.txt', 'r').read().strip()
        print(FLAG)
    else:
        print('Hmm not quite.')


if __name__ == '__main__':
    signal.alarm(10)
    main()
