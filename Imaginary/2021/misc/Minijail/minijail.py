MAX = 37

x = input(">>> ").strip()
assert len(x) <= MAX
eval(x, {'__builtins__': {'print': print}})
