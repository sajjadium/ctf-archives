from random import getrandbits
from math import prod

HEARTS = "🂱🂲🂳🂴🂵🂶🂷🂸🂹🂺🂻🂽🂾"
SPADES = "🂡🂢🂣🂤🂥🂦🂧🂨🂩🂪🂫🂭🂮"
DIAMONDS = "🃁🃂🃃🃄🃅🃆🃇🃈🃉🃊🃋🃍🃎"
CLUBS = "🃑🃒🃓🃔🃕🃖🃗🃘🃙🃚🃛🃝🃞"
DECK = SPADES+HEARTS+DIAMONDS+CLUBS  # Bridge Ordering of a Deck
ALPHABET52 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnop_rstuvw{y}"

CARDS_PER_DEAL = 25
assert CARDS_PER_DEAL % 2 == 1
MAX_DEAL = prod(x for x in range(len(DECK) - CARDS_PER_DEAL + 1, len(DECK) + 1))
DEAL_BITS = MAX_DEAL.bit_length()

def text_from_cards(string):
    return string.translate(string.maketrans(DECK, ALPHABET52))

def deal_game():
    shuffle = getrandbits(DEAL_BITS) % MAX_DEAL
    deck = list(DECK)
    deal = ""
    while shuffle > 0:
        deal += deck.pop(shuffle % len(deck))
        shuffle //= len(deck) + 1
    while len(deal) < CARDS_PER_DEAL:
        deal += deck.pop(0)
    return deal

def print_puzzle():
    with open("cards.txt", "w") as cards_file:
        for i in range(750):
            table = deal_game()
            cards_file.write(f"Game {i+1}:\n")
            for i in range((CARDS_PER_DEAL - 5) // 2):
                cards_file.write(f"{i + 1}: {table[i * 2]}{table[i * 2 + 1]}  ")
            cards_file.write("\nTable: {}{}{} {} {}\n\n".format(*table[CARDS_PER_DEAL - 5:]))

