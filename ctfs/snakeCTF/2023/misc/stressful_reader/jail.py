#!/usr/bin/env python3
import os

banner = r"""
 _____ _                      __       _                       _
/  ___| |                    / _|     | |                     | |
\ `--.| |_ _ __ ___  ___ ___| |_ _   _| |   _ __ ___  __ _  __| | ___ _ __
 `--. \ __| '__/ _ \/ __/ __|  _| | | | |  | '__/ _ \/ _` |/ _` |/ _ \ '__|
/\__/ / |_| | |  __/\__ \__ \ | | |_| | |  | | |  __/ (_| | (_| |  __/ |
\____/ \__|_|  \___||___/___/_|  \__,_|_|  |_|  \___|\__,_|\__,_|\___|_|

"""


class Jail():
    def __init__(self) -> None:
        print(banner)
        print()
        print()
        print("Will you be able to read the $FLAG?")
        print("> ",end="")


        self.F = ""
        self.L = ""
        self.A = ""
        self.G = ""
        self.run_code(input())
        pass

    def run_code(self, code):

        badchars = [ 'c', 'h', 'j', 'k', 'n', 'o', 'p', 'q', 'u', 'w', 'x', 'y', 'z'
                   , 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'
                   , 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W'
                   , 'X', 'Y', 'Z', '!', '"', '#', '$', '%'
                   , '&', '\'', '-', '/', ';', '<', '=', '>', '?', '@'
                   , '[', '\\', ']', '^', '`', '{', '|', '}', '~'
                   , '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


        badwords = ["aiter", "any", "ascii", "bin", "bool", "breakpoint"
                   , "callable", "chr", "classmethod", "compile", "dict"
                   , "enumerate", "eval", "exec", "filter", "getattr"
                   , "globals", "input", "iter", "next", "locals", "memoryview"
                   , "next", "object", "open", "print", "setattr"
                   , "staticmethod", "vars", "__import__", "bytes", "keys", "str"
                   , "join", "__dict__", "__dir__", "__getstate__", "upper"]


        if (code.isascii() and 
            all([x not in code for x in badchars]) and 
            all([x not in code for x in badwords])):

            exec(code)
        else:
            print("Exploiting detected, plz halp :/")

    def get_var(self, varname):
        print(os.getenv(varname))

if (__name__ == "__main__"):
    Jail()
