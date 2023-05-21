inp = input("code> ")[:72]
if "__" in inp:
    print("Nope")
else:
    print(eval(inp, {"__builtins__": {}}, {"__builtins__": {}}))