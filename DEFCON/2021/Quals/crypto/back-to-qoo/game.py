"""
This is a public file
"""
import random
from coin import Coin

GAME_DESCRIPTION = \
        "zardus: Hey hacker! Shall we play a game against QOO?\n" \
        "        There are two competitors here and they each will bet on 0 or 1.\n" \
        "        Let's put our numbers there so that the sum of ours is same as " \
        "the multiplication of theirs"

OPTIONS = "0. Bet for 0\n" \
        "1. Bet for 1\n" \
        "2. Use your magic qoin"
ZERO = "0"
ONE = "1"
COIN = "2"

COIN_ROTATE = "Do you want to rotate your qoin before flipping?\n" \
        "0. No, do not rotate my qoin\n" \
        "1. Yes, rotate left\n" \
        "2. Yes, rotate right"
NOT_CHANGE = "0"
LEFT = "1"
RIGHT = "2"

WIN = 1
LOSE = 0
WIN_MSG = "Win!"
LOSE_MSG = "Lose!"


class Game(object):
    def __init__(self, hacker, zardus, id):
        self.player1 = hacker
        self.player2 = zardus
        self.competitor_bet1 = random.randint(0, 1)
        self.competitor_bet2 = random.randint(0, 1)
        self.player2_bet = self.player2.bet(id, self.competitor_bet2)
        self.coin = Coin(id)
        self.id = id

    def error(self):
        print(f"Selection does not exist. {LOSE_MSG}")
        return LOSE

    def run(self):
        print(f"[Round {self.id}]: Your competitor bets on {self.competitor_bet1}")
        print(OPTIONS)
        selection = input().strip()
        if selection == COIN:
            print(COIN_ROTATE)
            selection = input().strip()
            if selection == LEFT:
                self.coin.rotate_left()
            elif selection == RIGHT:
                self.coin.rotate_right()
            elif selection != NOT_CHANGE:
                return self.error()
            player1_bet = self.coin.flip()  # Just clean it up. Not a hint.
        elif selection == ZERO:
            player1_bet = 0
        elif selection == ONE:
            player1_bet = 1
        else:
            return self.error()

        print(f"[Round {self.id}]: zardus's competitor bets on {self.competitor_bet2}, " +
                f"you bet on {player1_bet}")
        return self.play(player1_bet, self.player2_bet)

    def play(self, p1_bet, p2_bet):
        if p1_bet ^ p2_bet == self.competitor_bet1 * self.competitor_bet2:
            print(WIN_MSG)
            return WIN
        else:
            print(LOSE_MSG)
            return LOSE
