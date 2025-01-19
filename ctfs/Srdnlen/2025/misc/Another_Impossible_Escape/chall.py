#!/usr/bin/env python3
import sys
import re

BANNER = r"""
############################################################
#       _                _   _                             #
#      / \   _ __   ___ | |_| |__   ___ _ __               #
#     / _ \ | '_ \ / _ \| __| '_ \ / _ \ '__|              #
#    / ___ \| | | | (_) | |_| | | |  __/ |                 #
#   /_/   \_\_| |_|\___/ \__|_| |_|\___|_|                 #
#      ___                               _ _     _         #
#     |_ _|_ __ ___  _ __   ___  ___ ___(_) |__ | | ___    #
#      | || '_ ` _ \| '_ \ / _ \/ __/ __| | '_ \| |/ _ \   #
#      | || | | | | | |_) | (_) \__ \__ \ | |_) | |  __/   #
#     |___|_| |_| |_| .__/ \___/|___/___/_|_.__/|_|\___|   #
#    _____          |_|                                    #
#   | ____|___  ___ __ _ _ __   ___                        #
#   |  _| / __|/ __/ _` | '_ \ / _ \                       #
#   | |___\__ \ (_| (_| | |_) |  __/   (Author: @uNickz)   #
#   |_____|___/\___\__,_| .__/ \___|                       #
#                       |_|                                #
#                                                          #
############################################################
""" 

FLAG = "srdnlen{fake_flag}"
del FLAG

class IE:
    def __init__(self) -> None:
        print(BANNER)
        print("Welcome to another Impossible Escape!")
        print("This time in a limited edition! More information here:", sys.version)

        self.try_escape()
        return

    def code_sanitizer(self, dirty_code: str) -> str:
        if len(dirty_code) > 60:
            print("Code is too long. Exiting.")
            exit()

        if not dirty_code.isascii():
            print("Alien material detected... Exiting.")
            exit()

        banned_letters = ["m", "w", "f", "q", "y", "h", "p", "v", "z", "r", "x", "k"]
        banned_symbols = [" ", "@", "`", "'", "-", "+", "\\", '"', "*"]
        banned_words = ["input", "self", "os", "try_escape", "eval", "breakpoint", "flag", "system", "sys", "escape_plan", "exec"]

        if any(map(lambda c: c in dirty_code, banned_letters + banned_symbols + banned_words)):
            print("Are you trying to cheat me!? Emergency exit in progress.")
            exit()

        limited_items = {
            ".": 1,
            "=": 1,
            "(": 1,
            "_": 4,
        }

        for item, limit in limited_items.items():
            if dirty_code.count(item) > limit:
                print("You are trying to break the limits. Exiting.")
                exit()

        cool_code = dirty_code.replace("\\t", "\t").replace("\\n", "\n")
        return cool_code

    def escape_plan(self, gadgets: dict = {}) -> None:
        self.code = self.code_sanitizer(input("Submit your BEST Escape Plan: ").lower())
        return eval(self.code, {"__builtins__": {}}, gadgets)

    def try_escape(self) -> None:
        tries = max(1, min(7, int(input("How many tries do you need to escape? "))))

        for _ in range(tries):
            self.escape_plan()

        return

if __name__ == "__main__":
    with open(__file__, "r") as file_read:
        file_data = re.sub(r"srdnlen{.+}", "srdnlen{REDATTO}", file_read.read(), 1)

    with open(__file__, "w") as file_write:
        file_write.write(file_data)

    IE()