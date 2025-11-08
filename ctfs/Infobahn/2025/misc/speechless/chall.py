#!/usr/bin/python3

allowed = "ab.=-/"

with open("flag.txt", 'rb') as f:
    flag = f.read()

a = None
while True:
    expr = input(">>> ")

    if not all(char in allowed for char in expr):
        print('you need to try harder')
        continue

    if any(f"{blocked}==" in expr or f"=={blocked}" in expr for blocked in "ab"):
        print('stop comparing the flag')
        continue

    try:
        a = eval(expr, {"a": a} | {"b" * (index + 1): char for index, char in enumerate(flag)})
    except:
        a = None
        print('stop breaking things >:(')