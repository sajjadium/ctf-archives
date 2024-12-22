#!/usr/bin/env python3

import random
from collections import Counter
from numpy import poly1d
from queue import PriorityQueue
from src.secret import flag, coeff

assert len(flag) == 49
assert len(coeff) == 6
assert all(x > 0 and isinstance(x, int) for x in coeff)

P = poly1d(coeff)


class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right

    def __lt__(self, nxt):
        if self.freq == nxt.freq:
            return self.symbol < nxt.symbol

        return self.freq < nxt.freq


def get_codes(codes, node=None, val=""):
    if node:
        if not node.left and not node.right:
            codes[node.symbol] = val
        else:
            get_codes(codes, node.left, val + '0')
            get_codes(codes, node.right, val + '1')


def compress(s: str) -> str:
    cnt = Counter(s)
    codes = {}

    pq = PriorityQueue()
    for element in cnt:
        pq.put(Node(cnt[element], element))

    n_nodes = len(cnt)
    while n_nodes > 1:
        left = pq.get()
        right = pq.get()
        new = Node(left.freq + right.freq,
                   min(left.symbol, right.symbol), left, right)
        pq.put(new)
        n_nodes -= 1

    get_codes(codes, node=pq.get())

    cmprsd = ""
    for c in s:
        cmprsd += codes[c]

    # return cmprsd, codes
    return cmprsd


def get_info() -> int:
    s = list(flag)
    idx = random.randint(0, len(flag)-1)
    return P(ord(s[idx]))


def main():
    print("Welcome, agent, to the Decompressor Challenge!")
    print("Your mission, should you choose to accept it, involves unraveling the encrypted flag.")
    print("Can you decompress the flag without the codes?")
    print("Good luck, and may the odds be ever in your favor!\n")

    while True:
        print("Select your next action:")
        print("1. Retrieve compressed flag without codes.")
        print("2. Access additional intel.")
        print("3. Abort mission and exit.")

        choice = input("> ")
        if choice == "1":
            code = compress(flag)
            print(f"Compressed Flag: {code}")

        elif choice == "2":
            info = get_info()
            print(f"Additional Info: {info}")

        elif choice == "3":
            print("Mission aborted. Goodbye!")
            break

        else:
            print("Invalid choice! Please select a valid option.")
