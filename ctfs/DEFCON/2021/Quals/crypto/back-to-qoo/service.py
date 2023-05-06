#!/usr/bin/env python3
"""
This is a public file
"""
from players import zardus, hacker, adamd
from game import Game, WIN, LOSE, GAME_DESCRIPTION
from backend import setup_game, setup_chat, stop


PLAYS = 128
THRESHOLD = 0.85


def game(hacker, zardus):
    game_network = setup_game(hacker, zardus, PLAYS)

    print(GAME_DESCRIPTION)
    win = 0
    for i in range(PLAYS):
        g = Game(hacker, zardus, i)
        result = g.run()
        if result == WIN:
            win += 1

    print(f"your winning rate: {win / PLAYS}")
    if (win / PLAYS) > THRESHOLD:
        print("zardus: очень хороший! You are my true good friend.")
        print("        I am gonna share with you my chat with adamd.")
        print("        Shhhh, don't let him know.")
        return game_network, WIN
    else:
        print("zardus: You gotta win more, my friend. Bye!")
        return game_network, LOSE


def chat(zardus, adamd):
    chat_network = setup_chat(zardus, adamd, PLAYS)
    return chat_network


def main():
    game_network, result = game(hacker, zardus)
    if result == WIN:
        chat_network = chat(zardus, adamd)
        stop([game_network, chat_network])
    else:
        stop([game_network])


if __name__ == "__main__":
    main()
    exit(0)
