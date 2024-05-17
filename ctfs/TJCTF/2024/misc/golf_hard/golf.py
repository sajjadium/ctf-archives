#!/usr/local/bin/python3.11

import regex  # le duh
import os
import tomllib
from tabulate import tabulate
from importlib import import_module
from itertools import zip_longest as zp


def check_regex(pattern, matches, nonmatches):
    try:
        re = regex.compile(pattern, flags=regex.V1)
    except:
        print("nope")
        return False

    for text in matches:
        if not re.search(text):
            print(f"whoops, didn't match on {text}")
            return False

    for text in nonmatches:
        if re.search(text):
            print(f"whoops, matched on {text}")
            return False

    return True


def main():
    for dir in sorted(os.listdir("challenges")):
        tomlpath = os.sep.join(["challenges", dir, "info.toml"])
        with open(tomlpath, "rb") as f:
            info = tomllib.load(f)

        matches = info["matches"]
        nonmatches = info["nonmatches"]
        length = info["length"]

        print(info["description"])
        print(
            tabulate(
                zp(matches, nonmatches),
                [
                    "Match on all of these:",
                    "But none of these:    ",
                ],
                disable_numparse=True,
                tablefmt="simple",
            )
        )
        print(f"\nMaximum allowable length is {length}\n")

        # include some test cases that may be inconvenient to display
        # only some challenges have extra tests
        # fear not, the intended pattern will remain the same
        ext = import_module(f"challenges.{dir}.extensions")
        matches.extend(ext.more_matches())
        nonmatches.extend(ext.more_nonmatches())

        pattern = input("> ")
        if len(pattern) > length:
            print(f"whoops, too long")
            return

        if not check_regex(pattern, matches, nonmatches):
            return

    print(open("flag.txt").read())


if __name__ == "__main__":
    main()
