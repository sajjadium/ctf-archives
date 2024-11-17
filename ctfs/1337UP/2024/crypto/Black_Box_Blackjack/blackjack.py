#!/usr/bin/env python3

import os
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes

FLAG = os.getenv("FLAG", "INTIGRITI{REDACTED}").encode()


class HandStates:
    OKAY = 0,
    STANDING = 1,
    BUST = 2,
    BLACKJACK = 3,

    @staticmethod
    def get_state(score):
        if score > 21:
            return HandStates.BUST
        elif score == 21:
            return HandStates.BLACKJACK
        return HandStates.OKAY


class Card:
    VALUE_TO_NAME = {
        1: "Ace",
        11: "Jack",
        12: "Queen",
        13: "King",
    }

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        name = self.VALUE_TO_NAME.get(self.value, str(self.value))
        return f"{name} of {self.suit}"


class Deck:
    def __init__(self, seed):
        self.seed = seed
        self.reset()

    def reset(self):
        self.cards = []
        self.build()
        self.shuffle()

    def build(self):
        for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]:
            for value in range(1, 14):
                self.cards.append(Card(suit, value))

    def shuffle(self):
        new_cards = []
        for i in range(52):
            card_index = self.seed % (52 - i)
            new_cards.append(self.cards.pop(card_index))
            self.seed //= (52 - i)
        self.cards = new_cards

    def deal(self):
        if len(self.cards) == 0:
            self.reset()
        return self.cards.pop(0)


class Blackjack:
    def __init__(self, player_names, seed):
        self.player_names = player_names
        self.player_moneys = [0] * len(player_names)
        self.num_players = len(player_names)
        self.deck = Deck(seed)

    def setup_hands(self):
        self.hand_states = [HandStates.OKAY] * (self.num_players + 1)
        self.hands = [[self.deck.deal(), self.deck.deal()]
                      for _ in range(self.num_players + 1)]
        for i, hand in enumerate(self.hands):
            score = sum(card.value for card in hand)
            state = HandStates.get_state(score)
            self.hand_states[i] = state

    def play_round(self):
        print(f"Dealer ({self.hands[0][0].value}):")
        print("- " + str(self.hands[0][0]))
        print("- HIDDEN")
        print()

        for i in range(1, self.num_players + 1):
            self.show_hands(i)

        for i in range(1, self.num_players + 1):
            if self.hand_states[i] != HandStates.OKAY:
                continue
            name = self.player_names[i - 1]
            is_hit = False
            if i == 1:
                action = input("Hit or stand? ").lower()
                if action == "hit":
                    is_hit, state, card = (True, *self.hit(1))
            else:
                is_hit, state, card = self.choose_action(i)
            if is_hit:
                if state == HandStates.BLACKJACK:
                    print(f"{name} hit {card} and got a blackjack!")
                    self.hand_states[i] = HandStates.BLACKJACK
                elif state == HandStates.BUST:
                    print(f"{name} hit {card} and went bust!")
                    self.hand_states[i] = HandStates.BUST
                else:
                    print(f"{name} hits {card}!")
            else:
                print(f"{name} stands.")
                self.hand_states[i] = HandStates.STANDING
        print("\n" + "-" * 48 + "\n")

    def show_hands(self, hand_index):
        name = self.player_names[hand_index - 1] if hand_index > 0 else "Dealer"
        hand = self.hands[hand_index]
        score = sum(card.value for card in hand)
        state = HandStates.get_state(score)
        if state == HandStates.BLACKJACK:
            print(f"{name} ({score}): Blackjack!")
        elif state == HandStates.BUST:
            print(f"{name} ({score}): Bust!")
        elif state == HandStates.STANDING:
            print(f"{name} ({score}): Standing")
        else:
            print(f"{name} ({score}):")
        for card in hand:
            print("- " + str(card))
        print()

    def get_score(self, hand):
        return sum(card.value for card in hand)

    def hit(self, hand_index):
        hand = self.hands[hand_index]
        card = self.deck.deal()
        hand.append(card)
        return (HandStates.get_state(self.get_score(hand)), card)

    def choose_action(self, hand_index):
        score = self.get_score(self.hands[hand_index])
        if score < 17:
            return (True, *self.hit(hand_index))
        return (False, HandStates.STANDING, None)

    def are_any_players_okay(self):
        return any([state == HandStates.OKAY for state in self.hand_states[1:]])

    def play_dealer(self):
        self.show_hands(0)
        state = self.hand_states[0]
        is_action_made = False
        while state == HandStates.OKAY:
            is_action_made = True
            is_hit, state, card = self.choose_action(0)
            if is_hit:
                print(f"Dealer hits {card}!")
            else:
                print("Dealer stands.")
        if is_action_made:
            self.hand_states[0] = state
            print()
            self.show_hands(0)

    def str_money(self, money):
        if money < 0:
            return f"-${abs(money)}"
        return f"€{money}"

    def show_results(self):
        dealer_score = self.get_score(self.hands[0])
        dealer_state = self.hand_states[0]
        for i in range(1, self.num_players + 1):
            name = self.player_names[i - 1]
            score = self.get_score(self.hands[i])
            state = self.hand_states[i]
            money = self.player_moneys[i - 1]
            if state == HandStates.BLACKJACK:
                money += 100
                print(f"{name} got a blackjack! {self.str_money(money)}")
            elif state == HandStates.BUST:
                money -= 75
                print(f"{name} went bust! {self.str_money(money)}")
            elif dealer_state == HandStates.BUST or score > dealer_score:
                money += 50
                print(f"{name} beat the dealer! {self.str_money(money)}")
            else:
                money -= 50
                print(f"{name} lost to the dealer! {self.str_money(money)}")
            self.player_moneys[i - 1] = money

    def show_final_winner(self):
        max_money = max(self.player_moneys)
        winners = [name for name, money in zip(self.player_names, self.player_moneys) if money == max_money]
        if len(winners) == 1:
            print(f"The winner is {winners[0]}!")
        else:
            print(f"The winners are {', '.join(winners)}!")
        if self.player_moneys[0] < 0:
            print("Looks like you are in the red :(")
            print("Better luck next time!")
        elif self.player_moneys[0] == max_money:
            print("Congrats on winning!")
        else:
            print("Thanks for playing!")


class Crypto:
    def __init__(self, n_bits):
        REDACTED

    def encrypt(self, data):
        REDACTED


def run(game):
    game.setup_hands()
    game.play_round()
    while game.are_any_players_okay():
        game.play_round()
    print("Dealer's turn!\n")
    print("-" * 48 + "\n")
    game.play_dealer()
    print("Game over!\n")
    print("-" * 48 + "\n")
    game.show_results()
    print("\n" + "-" * 48 + "\n")


if __name__ == "__main__":
    crypto = Crypto(350)

    print(""" /$$$$$$$  /$$                     /$$       /$$$$$$$                     
| $$__  $$| $$                    | $$      | $$__  $$                    
| $$  \ $$| $$  /$$$$$$   /$$$$$$$| $$   /$$| $$  \ $$  /$$$$$$  /$$   /$$
| $$$$$$$ | $$ |____  $$ /$$_____/| $$  /$$/| $$$$$$$  /$$__  $$|  $$ /$$/
| $$__  $$| $$  /$$$$$$$| $$      | $$$$$$/ | $$__  $$| $$  \ $$ \  $$$$/ 
| $$  \ $$| $$ /$$__  $$| $$      | $$_  $$ | $$  \ $$| $$  | $$  >$$  $$ 
| $$$$$$$/| $$|  $$$$$$$|  $$$$$$$| $$ \  $$| $$$$$$$/|  $$$$$$/ /$$/\  $$
|_______/ |__/ \_______/ \_______/|__/  \__/|_______/  \______/ |__/  \__/
""")
    print("Welcome to the Black Box casino!")
    name = input("What is your name? ")
    print("As this is the Black Box casino, I will not be telling you my name.")
    print("Although my name encrypted is:", crypto.encrypt(FLAG).hex())
    print("Not that you will be able to decrypt it anyways...")
    print("After all, you don't even know what cryptosystem I am using!\n")
    print("=" * 48 + "\n")
    print("LET'S BEGIN!\n")

    names = [name, "Alice", "Bob", "Eve",
             "Mallory", "Trent", "Samuel", "Amber"]
    print("Welcome to the table!")
    print("You will be playing against the following players:")
    for n in names[1:]:
        print(f"- {n}")
    print("You will be playing three rounds of Blackjack.")
    print("The player with the most money at the end wins!")
    print("I hope nobody ends up in the red ;)\n")
    print("-" * 48 + "\n")

    seed = bytes_to_long(crypto.encrypt(name.encode(errors="surrogateescape")))
    game = Blackjack(names, seed)
    run(game)
    print("Let's play again!\n")
    print("-" * 48 + "\n")
    run(game)
    print("One last time!\n")
    print("-" * 48 + "\n")
    run(game)
    game.show_final_winner()
