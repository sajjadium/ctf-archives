#!/usr/bin/env python3

import re
from sys import modules, version

banned = "import|chr|os|sys|system|builtin|exec|eval|subprocess|pty|popen|read|get_data"
search_func = lambda word: re.compile(r"\b({0})\b".format(word), flags=re.IGNORECASE).search

modules.clear()
del modules

def main():
    print(f"{version}\n")
    print("What would you like to say?")
    for _ in range(2):
        text = input('>>> ').lower()
        check = search_func(banned)(''.join(text.split("__")))
        if check:
            print(f"Nope, we ain't letting you use {check.group(0)}!")
            break
        if re.match("^(_?[A-Za-z0-9])*[A-Za-z](_?[A-Za-z0-9])*$", text):
            print("You aren't getting through that easily, come on.")
            break
        else:
            exec(text, {'globals': globals(), '__builtins__': {}}, {'print':print})

if __name__ == "__main__":
    main()
