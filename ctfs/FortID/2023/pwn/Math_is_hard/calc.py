#!/usr/bin/python3

from math import *
from string import *

USAGE = """PwnCalc -- a simple calculator
$ a=4
>>> a = 4
$ a = 4
>>> a = 4
$ b = 3
>>> b = 3
$ c = sqrt(a*a+b*b)
>>> c = 5.0
$ d = sin(pi/4)
>>> d = 0.7071067811865475
Have fun!
"""

def check_expression(s):
    """Allow only digits, decimal point, lowecase letters and math symbols."""
    SYMBOLS = ".+*-/()"
    for c in s:
        if not c.islower() and not c.isdigit() and c not in SYMBOLS:
            return False
    return True

def loop():
    """Main calculator loop."""
    vars = { c : 0 for c in ascii_lowercase }
    while True:
        line = input("$ ")
        if not line:
            print("Bye!")
            return
        items = line.split("=")
        if len(items) != 2:
            print("Invalid syntax!")
            continue
        varname, expression = items
        varname = varname.strip()
        expression = expression.strip()
        if len(varname) != 1 or not varname.islower():
            print("Invalid variable name!")
            continue
        if not check_expression(expression):
            print("Invalid character in expression!")
            continue
        result = eval(expression, vars, {'sin': sin, 'cos': cos, 'sqrt': sqrt, 'exp': exp, 'log': log, 'pi': pi})
        vars[varname] = result
        print(">>> {} = {}".format(varname, result))


if __name__ == "__main__":
    print(USAGE)
    loop()
