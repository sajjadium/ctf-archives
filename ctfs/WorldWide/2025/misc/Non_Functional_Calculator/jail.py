#!/usr/local/bin/python

values = {}
whitelist_chars = set("abcdefghijklmnopqrstuvwxyz0123456789.,()")
blacklist_words = {
    "exe",
    "import",
    "eval",
    "os",
    "sys",
    "run",
    "sub",
    "class",
    "process",
    "cat",
    "repr",
    "base",
    "echo",
    "open",
    "file",
    "sh",
    "item",
    "call",
    "spawn",
    "output",
    "status",
    "load",
    "module",
    "reduce",
    "builtins",
    "locals",
    "globals",
}

variable_name = ""
variable_value = ""


def calculate(equation):
    global variable_name, variable_value

    if not len(equation) != 0:
        print("There is no equation for me to run... (╥﹏╥)")
        exit()

    equation = equation.encode().decode("ascii", errors="ignore")

    if "=" in equation:
        value_name, equation = equation.split("=", 1)

        if not (len(value_name) == 1 and value_name in whitelist_chars):
            print("Bad characters detected! (-`д´-)")
            exit()

        equation = equation.strip()
    else:
        value_name = ""

    if not set(equation).issubset(whitelist_chars):
        print("Non whitelisted characters in equation (╯°□°）╯︵ ┻━┻")
        exit()

    for i in blacklist_words:
        if i in equation.lower():
            print("Blacklisted words in equation (╯°□°）╯︵ ┻━┻")
            exit()

    equation = equation.replace(variable_name, variable_value)

    try:
        result = eval(equation, {"__builtins__": None})
    except:
        print("Invalid equation (´；ω；`)")
        exit()

    if value_name:
        variable_name = str(value_name.strip())
        variable_value = str(result)
        print(f"Saved {value_name} = {result}")
    else:
        print(f"Result: {result}")


for _ in range(2):
    calculate(input("Equation: "))
