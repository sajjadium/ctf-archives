#!/usr/bin/python3
import re
import random

code = input("Let's Start: ")

if re.match(r"[a-zA-Z]{4}", code):
    print("Code failed, restarting...")

elif len(set(re.findall(r"[\W]", code))) > 4:
    print(set(re.findall(r"[\W]", code)))
    print("A single code cannot process this much special characters. Restarting.")

else:
    discovery = list(eval(compile(code, "<code>", "eval").replace(co_names=())))
    random.shuffle(discovery)
    print("You compiled it, but are severely overloaded. This is all CPU can hold:", discovery)
