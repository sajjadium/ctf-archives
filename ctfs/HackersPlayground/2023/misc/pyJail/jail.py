import string

flag = open("./flag.txt").read()
code = input("makeflag> ")[:100]

if any(c not in string.printable for c in code):
    print("🙅")
elif "__" in code:
    print("__nope__")
else:
    if flag == eval(code, {"__builtins__": {}}, {"__builtins__": {}}):
        print("Oh, you know flag")
    else:
        print("Nope")
