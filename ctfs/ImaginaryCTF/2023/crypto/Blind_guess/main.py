from random import getrandbits
from galois import GF
import numpy as np

DECK = "🂡🂢🂣🂤🂥🂦🂧🂨🂩🂪🂫🂭🂮"
F = GF(13) # lucky number
n = 10

# Let's not use a singular matrix, please.
# We do quality random over here.
M = [[0]]
while np.linalg.det(M) == 0:
    M = F.Random((n, n))

money = 15000
cards = F.Random(n)
while all(int(c) == 0 for c in cards):
    cards = F.Random(n)

while money > 0:
    print('balance:', money)
    choice = input('> ')

    if choice == 'buy flag':
        if money < 1_000_000_000:
            print("You're too poor!")
            continue

        from redacted import FLAG
        money -= 1_000_000_000
        print("What a guess god! Here's your flag:", FLAG)

    elif choice == 'play':
        bet = int(input('bet: '))
        assert money >= bet > 0
        print("Can you blindly guess my cards?")

        cards = np.linalg.matrix_power(M, getrandbits(32)) @ cards  # shuffle cards
        guess = M @ F([*map(DECK.index, input('guess: ').split())]) # blind guess
        total = sum(cards == guess)

        print(f'You guessed {total} cards! My hand was:', *[DECK[c] for c in cards])
        money += 2*(total - 5)*bet
    
    elif choice == 'exit':
        print("Chickened out, huh? No flag for you.")
        exit()

print("Woops... Looks like you guessed your way out of money :>")