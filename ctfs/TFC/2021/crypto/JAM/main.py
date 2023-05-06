#!/usr/bin/env python3
import random
import re
import string
import sys

from secret import secret, flag
import hashlib


def print_trade_help():
    print("----=== Trade ===----")
    print("1. Flag - 6 COIN(S)")
    print("2. Random String - 1 COIN(S)")
    print("3. Nothing - 1 COIN(S)")
    print("---------------------")


def print_help():
    print("----=== Menu ===----")
    print("1. Work!")
    print("2. Trade!")
    print("3. Recover last session!")
    print("4. Check your purse!")
    print("5. Print recovery token!")
    print("q. Quit!")
    print("--------------------")


class Console:
    def __init__(self):
        self.__secret = secret.encode("utf-8")
        self.__hash = hashlib.md5(self.__secret + b' 0').hexdigest()
        self.__coins = 0

    def work(self):
        if self.__coins >= 5:
            print("Can't work anymore! You're too tired!")
            return

        self.__coins += 1
        print("You've worked really hard today! Have a coin!")
        print("Purse: " + str(self.__coins) + " (+1 COIN)")
        self.__hash = hashlib.md5(self.__secret + b' ' + str(self.__coins).encode("utf-8")).hexdigest()
        print("To recover, here's your token: " + self.__hash)

    def trade(self):
        options = {
            "1": (6, flag),
            "2": (1, ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))),
            "3": (1, "You receive nothing.")
        }
        print_trade_help()
        print("What would you like to buy?")
        opt = input("> ")
        if opt not in options.keys():
            print("Invalid option!")
            return
        if options[opt][0] > self.__coins:
            print("You do not have enough coins!")
            return
        else:
            self.__coins -= options[opt][0]
            print(options[opt][1])
            print("Purse: " + str(self.__coins) + " (-" + str(options[opt][0]) + " COIN(S))")

    def recover(self):
        print("In order to recover, we need two things from you.")
        print("1. How many coins did you have?")
        print("> ", end="")
        amt_coins = sys.stdin.buffer.readline()[:-1]
        print("2. What was your recovery token?")
        token = input("> ")
        hash_tkn = self.__secret + b" " + amt_coins
        hash_for_coins = hashlib.md5(hash_tkn).hexdigest()
        if hash_for_coins != token:
            print("Incorrect!")
            return
        self.__coins = int(re.sub("[^0-9]", "", amt_coins.decode("unicode_escape")))
        print(self.__coins)
        self.__hash = token
        print("Recovered successfully!")

    def check_purse(self):
        print("Purse: " + str(self.__coins))

    def get_recovery_token(self):
        print(self.__hash)

    def start_console(self):
        options = {
            "1": self.work,
            "2": self.trade,
            "3": self.recover,
            "4": self.check_purse,
            "5": self.get_recovery_token,
        }

        while True:
            print_help()
            inp = input("> ")
            if inp == "q":
                print("Quitting.")
                sys.exit(0)
            if inp not in options.keys():
                print("Not a valid option!")
                continue
            try:
                options[inp]()
            except Exception:
                pass


if __name__ == "__main__":
    console = Console()
    console.start_console()
