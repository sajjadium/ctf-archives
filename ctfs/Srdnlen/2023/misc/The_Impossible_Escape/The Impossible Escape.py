from os import getenv

banner = r"""
#############################################################################
#    _____ _            ___                               _ _     _         #
#   |_   _| |__   ___  |_ _|_ __ ___  _ __   ___  ___ ___(_) |__ | | ___    #
#     | | | '_ \ / _ \  | || '_ ` _ \| '_ \ / _ \/ __/ __| | '_ \| |/ _ \   #
#     | | | | | |  __/  | || | | | | | |_) | (_) \__ \__ \ | |_) | |  __/   #
#    _|_|_|_| |_|\___| |___|_| |_| |_| .__/ \___/|___/___/_|_.__/|_|\___|   #
#   | ____|___  ___ __ _ _ __   ___  |_|                                    #
#   |  _| / __|/ __/ _` | '_ \ / _ \                                        #
#   | |___\__ \ (_| (_| | |_) |  __/           (Author: @uNickz)            #
#   |_____|___/\___\__,_| .__/ \___|                                        #
#                       |_|                                                 #
#                                                                           #
#############################################################################
"""

class TIE:
    def __init__(self) -> None:
        print(banner)
        self.flag = getenv("FLAG", "srdnlen{REDACTED}")
        self.code = self.code_sanitizer(input("Submit your BEST (and perhaps only) Escape Plan: "))
        self.delete_flag()
        exec(self.code)

    def code_sanitizer(self, dirty_code: str) -> str:
        if not dirty_code.isascii():
            print("Alien material detected... Exiting.")
            exit()

        banned_letters = ["m", "o", "w", "q", "b", "y", "u", "h", "c", "v", "z", "x", "k", "g"]
        banned_symbols = ["}", "{", "[", "]", ":", " ", "&", "`", "'", "-", "+", "\\", ".", "="]
        banned_words = ["flag", ]

        if any(map(lambda c: c in dirty_code, banned_letters + banned_symbols + banned_words)):
            print("Are you trying to cheat me!? Emergency exit in progress.")
            exit()

        cool_code = dirty_code.replace("\\t", "\t").replace("\\n", "\n")
        return cool_code

    def delete_flag(self) -> None:
        self.flag = "You cant grab me ;)"
        print("Too slow... what you were looking for has just been destroyed.")

if __name__ == "__main__":
    TIE()