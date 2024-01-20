#!/usr/bin/env python3

import string
import subprocess
import sys
import os

import gui

alphabet = "abcdefghijklmnopqrstuvwxyz/,:;[]_-."

prefix = "/app/quizzes/"
results = prefix + "pts.txt"

def menu():
    print(gui.menu)

    choice = int(input("> "))
    if choice != 1 and choice != 2:
        exit(0)

    return choice

def get_user_string(text):
    print(text)
    s = input("> ").lower()
    for c in s:
        if c not in alphabet:
            exit(0)
    return s[:7]

def run_quizz(username, category):
    command = f"make run quizz=\"{prefix + category}\" username=\"{username}\""
    os.system(command)

def play():
    username = get_user_string(gui.username)
    category = get_user_string(gui.category)
    run_quizz(username, category)

# TODO: improve and combine categories scores
def scoreboard():
    scores = {}
    for line in open(results, 'r').readlines():
        k = line.split(' ')[0]
        v = int(line.strip().split(',')[-1][:-1])
        scores[k] = v
    scores = sorted(scores.items(), reverse=True, key=lambda item: item[1])

    print(gui.scoreboard_head)
    for i, r in enumerate(scores):
        print(f"      {i+1}. {r[0]}\t{r[1]}")
    print(gui.scoreboard_tail)

def main():
    while True:
        try:
            choice = menu()
            if choice == 1:
                play()
            elif choice == 2:
                scoreboard()
        except Exception:
            exit()

if __name__ == '__main__':
    main()
