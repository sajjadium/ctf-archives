#!/usr/bin/env python3
import sys


def bf(code):
    output = ""
    s = []
    matches = {}
    tape = [0] * 1000000
    for i, j in enumerate(code):
        if j == "[":
            s.append(i)
        if j == "]":
            m = s.pop()
            matches[m] = i
            matches[i] = m
    cp = 0
    p = 0
    while cp < len(code):
        if code[cp] == "+":
            tape[p] = (tape[p] + 1) % 256
        if code[cp] == "-":
            tape[p] = (tape[p] - 1) % 256
        if code[cp] == ",":
            c = sys.stdin.read(1)
            tape[p] = (ord(c) if c else 0) % 256
        if code[cp] == ".":
            output += chr(tape[p])
        if code[cp] == "<":
            p -= 1
        if code[cp] == ">":
            p += 1
        if code[cp] == "[":
            if not tape[p]:
                cp = matches[cp]
        if code[cp] == "]":
            if tape[p]:
                cp = matches[cp]
        cp += 1

    return output


if __name__ == "__main__":
    code = input("> ")
    if len(code) > 200:
        print("200 chars max")
        sys.exit(0)
    if not all(c in set("+-<>[],.") for c in code):
        print("nope")
        exit(0)
    code = bf(code)
    exec(code)
