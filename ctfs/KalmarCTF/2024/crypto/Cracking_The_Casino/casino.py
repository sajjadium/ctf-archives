#!/usr/bin/python3 
from Pedersen_commitments import gen, commit, verify


# I want to host a trustworthy online casino! 
# To implement blackjack and craps in a trustworthy way i need verifiable dice and cards!
# I've used information theoretic commitments to prevent players from cheating.
# Can you audit these functionalities for me ?

from random import randint
# Verifiable Dice roll
def roll_dice(pk):
    roll = randint(1,6)
    comm, r = commit(pk,roll)
    return comm, roll, r

# verifies a dice roll
def check_dice(pk,comm,guess,r):
    res = verify(pk,comm, r, int(guess))
    return res

# verifiable random card:
def draw_card(pk):
    idx = randint(0,51)
    # clubs spades diamonds hearts
    suits = "CSDH"
    values = "234567890JQKA"
    value = values[idx%13]
    suit = suits[idx//13]
    card = value + suit
    comm, r = commit(pk, int(card.encode().hex(),16))
    return comm, card, r

# take a card (as two chars, fx 4S = 4 of spades) and verifies it was the committed card
def check_card(pk, comm, guess, r):
    res = verify(pk, comm, r, int(guess.encode().hex(),16))
    return res


# Debug testing values for larger values
def debug_test(pk):
    dbg = randint(0,2**32-2)
    comm, r = commit(pk,dbg)
    return comm, dbg, r

# verify debug values
def check_dbg(pk,comm,guess,r):
    res = verify(pk,comm, r, int(guess))
    return res


def audit():
    print("Welcome to my (beta test) Casino!")
    q,g,h = gen()
    pk = q,g,h
    print(f'public key for Pedersen Commitment Scheme is:\nq = {q}\ng = {g}\nh = {h}')
    chosen = input("what would you like to play?\n[D]ice\n[C]ards")
    
    if chosen.lower() == "d":
        game = roll_dice
        verif = check_dice
    elif chosen.lower() == "c":
        game = draw_card
        verif = check_card
    else:
        game = debug_test
        verif = check_dbg

    correct = 0
    # If you can guess the committed values more than i'd expect, then 
    for _ in range(1337):
        if correct == 100:
            print("Oh wow, you broke my casino??!? Thanks so much for finding this before launch so i don't lose all my money to cheaters!")
            with open("flag.txt","r") as f:
                flag = f.read()
            print(f"here's that flag you wanted, you earned it! {flag}")
            exit()

        comm, v, r = game(pk)
        print(f'Commitment: {comm}')
        g = input(f'Are you able to guess the value? [Y]es/[N]o')
        if g.lower() == "n":
            print(f'commited value was {v}')
            print(f'randomness used was {r}')
            print(f'verifies = {verif(pk,comm,v,r)}')
        elif g.lower() == "y":
            guess = input(f'whats your guess?')
            if verif(pk, comm, guess, r):
                correct += 1
                print("Oh wow! well done!")
            else:
                print("That's not right... Why are you wasting my time if you haven't broken anything?")
                exit()

    print(f'Guess my system is secure then! Lets go ahead with the launch!')
    exit()

if __name__ == "__main__":
    audit()
